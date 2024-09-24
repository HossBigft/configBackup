import argparse
from dns import resolver, reversename
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
    
    print(f"Trying to find {domain} host by A record")
    try:
        a_record = "".join([ipval.to_text() for ipval in resolver.resolve(domain, "A")])
        try:
            addr_record = reversename.from_address(a_record)
            ptr_record = str(resolver.resolve(addr_record, "PTR")[0])
            if "hoster.kz" in ptr_record:
                print(ptr_record, end="")
                sys.exit(0)
            else:
                print(f"No substring 'hoster.kz' in {ptr_record}")
        except resolver.NXDOMAIN:
            print(f"There is no PTR record for {a_record}")
    except resolver.NXDOMAIN:
        print(f"There is no A record for {domain}")



    # try:
    #     command = shlex.split(f'fish -c "nsZoneMaster -q {domain}"')

    #     output = subprocess.run(command, capture_output=True, text=True, check=True)
    #     domainPtr = socket.getfqdn(socket.gethostbyname(output.stdout))
    #     if not domainPtr[-1] == ".":
    #         domainPtr += "."
    #     if "hoster.kz" in domainPtr:
    #         print(domainPtr, end="")
    #         sys.exit(0)
    # except Exception as e:
    #     print(e)

    # try:
    #     command = shlex.split(f'python3 pFindSubscriptionByDomain.py -s {domain}"')

    #     output = subprocess.run(command, capture_output=True, text=True, check=True)
    #     host = output.stdout
    #     print (host)
    #     sys.exit(0)
    # except Exception as e:
    #     print(f"No servers was found with domain {domain}")
    #     sys.exit(1)


if __name__ == "__main__":
    main()
