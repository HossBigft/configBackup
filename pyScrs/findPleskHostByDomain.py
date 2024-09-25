import argparse
from dns import resolver, reversename
import sys
import nsZoneMaster
import pFindSubscriptionByDomain as pfind
import re

DNS_HOSTING_HOSTNAME = "dns.hoster.kz."


def regex_type(pattern: str | re.Pattern):
    """Argument type for matching a regex pattern."""

    def closure_check_regex(arg_value):
        if not re.match(pattern, arg_value):
            raise argparse.ArgumentTypeError(
                f"Invalid domain name: '{arg_value}' is not a valid domain name"
            )
        return arg_value

    return closure_check_regex


def main():
    parser = argparse.ArgumentParser(
        description="Tries to find Plesk server hostname by given domain"
    )

    parser.add_argument(
        "domain",
        type=regex_type(r"(?:(?!-|[^.]+_)[A-Za-z0-9-_]{1,63}(?<!-)(?:\.|$)){2,}"),
        help="domain name of the site to search",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="enables detailed output in the console",
    )
    args = parser.parse_args()
    domain = args.domain
    verbose_flag = args.verbose
    if verbose_flag:
        print(f"Starting host resolution for {domain} using A record.")



    if verbose_flag:
        print(f"Attempting to find host {domain} by querying servers.")
    if answers := [
        answer
        for answer in pfind.query_domain_info(domain, verbose_flag=False)
        if not answer["host"] == DNS_HOSTING_HOSTNAME
    ]:
        if (hosts_num := len(answers)) > 1:
            print(f"[ERROR] Multiple hosts found [{hosts_num}] The actual host is ambiguous.")
            for answer in answers:
                print(answer["host"])
            sys.exit(1)
        else:
            for answer in answers:
                print(answer["host"])
            sys.exit(0)
    else:
        if verbose_flag:
            print("[ERROR] Host for {domain} not found.")
        sys.exit(1)


if __name__ == "__main__":
    main()
