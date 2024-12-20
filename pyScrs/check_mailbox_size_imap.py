#!/usr/bin/env python3
import imaplib
import argparse
import getpass
import sys
import re
from datetime import datetime
import time


def log(message, debug=False):
    """Print debug message with timestamp if debug is enabled"""
    if debug:
        print(f"[DEBUG] {datetime.now().strftime('%H:%M:%S')}: {message}", file=sys.stderr)


def parse_mailbox_name(mailbox_str):
    """Extract clean mailbox name from IMAP list response"""
    match = re.search(r'"([^"]+)"$', mailbox_str)
    if match:
        return match.group(1)
    parts = mailbox_str.split('" "')
    if len(parts) > 1:
        return parts[-1].strip('"')
    return mailbox_str.split()[-1].strip('"')


def reconnect(host, username, password, port=993, max_retries=3):
    """Establish a new IMAP connection with retry logic"""
    for attempt in range(max_retries):
        try:
            imap = imaplib.IMAP4_SSL(host, port)
            imap.login(username, password)
            return imap
        except Exception as e:
            log(f"Connection attempt {attempt + 1} failed: {str(e)}", debug=True)
            if attempt < max_retries - 1:
                time.sleep(2**attempt)  # Exponential backoff
            else:
                raise
    return None


def get_folder_size(imap, mailbox_name, host, username, password, port, debug=False):
    """Get size of a single folder"""
    try:
        log(f"Selecting mailbox: {mailbox_name}", debug)
        status, select_data = imap.select(mailbox_name, readonly=True)

        if status != "OK":
            log(f"Failed to select mailbox {mailbox_name}: {select_data}", debug)
            return {"size": 0, "messages": 0}

        log("Searching for messages", debug)
        _, messages = imap.search(None, "ALL")
        if not messages[0]:
            log("No messages found in mailbox", debug)
            return {"size": 0, "messages": 0}

        message_nums = messages[0].split()
        total_size = 0
        batch_size = 100
        log(f"Found {len(message_nums)} messages, processing in batches of {batch_size}", debug)

        for i in range(0, len(message_nums), batch_size):
            try:
                batch = message_nums[i: i + batch_size]

                msg_range = ",".join(msg.decode() for msg in batch)
                _, sizes = imap.fetch(msg_range, "(RFC822.SIZE)")
                for size_data in sizes:
                    if isinstance(size_data, bytes):
                        size = int(
                            re.search(r"RFC822\.SIZE (\d+)", size_data.decode()).group(1)
                        )
                        total_size += size

                progress = min(i + batch_size, len(message_nums))
                sys.stderr.write(f"\rProcessing {mailbox_name}: {progress}/{len(message_nums)} messages...")
                sys.stderr.write(f"\nFolder size: {format_size(total_size)}")
                sys.stderr.flush()

            except Exception as e:
                log(f"Error during batch processing, attempting to reconnect: {str(e)}", debug)
                imap = reconnect(host, username, password, port)
                if imap is None:
                    raise Exception("Failed to reconnect")
                imap.select(mailbox_name, readonly=True)
                # Retry the current batch
                i -= batch_size
                continue

        if len(message_nums) > batch_size:
            sys.stderr.write("\n")

        return {"size": total_size, "messages": len(message_nums)}

    except Exception as e:
        log(f"Error processing mailbox {mailbox_name}: {str(e)}", debug)
        return {"size": 0, "messages": 0}


def check_mailbox_sizes(host, username, password, port=993, folder=None, debug=False):
    """Check sizes of all or specific mailboxes"""
    log(f"Connecting to {host}:{port}", debug)
    imap = reconnect(host, username, password, port)
    sizes = {}

    try:
        log("Getting list of mailboxes", debug)
        status, mailboxes = imap.list()

        if status == "OK":
            log(f"Found {len(mailboxes)} mailboxes", debug)
            mailbox_list = mailboxes
            if folder:
                mailbox_list = [m for m in mailboxes if folder in m.decode()]
                if not mailbox_list:
                    log(f"Error: Folder '{folder}' not found", debug)
                    return {}

            for mailbox in mailbox_list:
                mailbox_name = parse_mailbox_name(mailbox.decode())
                log(f"Processing mailbox: {mailbox_name}", debug)

                try:
                    result = get_folder_size(
                        imap, mailbox_name, host, username, password, port, debug
                    )
                    if result["messages"] > 0 or result["size"] > 0:
                        sizes[mailbox_name] = result
                except Exception as e:
                    log(
                        f"Error processing mailbox {mailbox_name}, trying to reconnect: {str(e)}", debug
                    )
                    imap = reconnect(host, username, password, port)
                    if imap is not None:
                        result = get_folder_size(
                            imap, mailbox_name, host, username, password, port, debug
                        )
                        if result["messages"] > 0 or result["size"] > 0:
                            sizes[mailbox_name] = result

        return sizes

    finally:
        try:
            log("Logging out", debug)
            imap.logout()
        except:
            pass


def format_size(size_bytes):
    """Convert bytes to human readable format"""
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} TB"


def main():
    parser = argparse.ArgumentParser(description="Check IMAP mailbox sizes")
    parser.add_argument("-s", "--server", required=True, help="IMAP server hostname")
    parser.add_argument("-u", "--username", required=True, help="Username")
    parser.add_argument(
        "-p", "--port", type=int, default=993, help="IMAP port (default: 993)"
    )
    parser.add_argument("-f", "--folder", help="Specific folder to check")
    parser.add_argument(
        "--password",
        help="Password (not recommended, use environment variable or prompt)",
    )
    parser.add_argument("--csv", action="store_true", help="Output in CSV format")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")

    args = parser.parse_args()

    # Remove trailing dot from server name if present
    server = args.server.rstrip(".")

    # Get password securely
    password = args.password
    if not password:
        password = getpass.getpass("Enter password: ")

    # Check sizes
    sizes = check_mailbox_sizes(server, args.username, password, args.port, args.folder, debug=args.debug)

    if not sizes:
        sys.exit(1)

    # Output results
    if args.csv:
        print("Folder,Size,Messages")
        for mailbox, info in sorted(sizes.items()):
            print(f"{mailbox},{info['size']},{info['messages']}")
    else:
        print("\nMailbox Sizes:")
        print("-" * 60)
        total_size = 0
        total_messages = 0

        for mailbox, info in sorted(sizes.items()):
            size = info["size"]
            messages = info["messages"]
            print(f"{mailbox}:")
            print(f"  Size: {format_size(size)}")
            print(f"  Messages: {messages:,}")
            total_size += size
            total_messages += messages

        print("-" * 60)
        print(f"Total size: {format_size(total_size)}")
        print(f"Total messages: {total_messages:,}")


if __name__ == "__main__":
    main()
