import argparse
import socket
import sys
import shlex
import subprocess


    
def main():
    parser = argparse.ArgumentParser(
        description="Tries to find Plesk server hostname by given domain"
    )

    parser.add_argument(
        "domain",
        type=str,
        help="Domain name of the site for search",
    )
    args = parser.parse_args()
    domain = args.domain
    try:
        domainPtr = socket.getfqdn(socket.gethostbyname(domain))
        if not domainPtr[-1] == ".":
            domainPtr += "."
        if "hoster.kz" in domainPtr:
            print(domainPtr, end="")
            sys.exit(0)

    except socket.gaierror:
        pass

    try:
        command = shlex.split(f'fish -c "nsZoneMaster -q {domain}"')

        output = subprocess.run(command, capture_output=True, text=True, check=True)
        domainPtr = socket.getfqdn(socket.gethostbyname(output.stdout))
        if not domainPtr[-1] == ".":
            domainPtr += "."
        if "hoster.kz" in domainPtr:
            print(domainPtr, end="")
            sys.exit(0)
    except Exception as e:
        print(e)

    try:
        command = shlex.split(f'python3 pFindSubscriptionByDomain.py -s {domain}"')

        output = subprocess.run(command, capture_output=True, text=True, check=True)
        host = output.stdout
        print (host)
        sys.exit(0)
    except Exception as e:
        print(f"No servers was found with domain {domain}")
        sys.exit(1)
        
if __name__ == "__main__":
    main()
