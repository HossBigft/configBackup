import argparse
import sys
from dns import resolver, reversename, exception
from ssh_zone_master import getDomainZoneMaster


SERVER_LIST = "DNS"
DNS_HOSTING_HOSTNAME = "dns.hoster.kz."


def getPtr(ip: str):
    try:
        addr_record = reversename.from_address(ip)
        ptr_record = str(resolver.resolve(addr_record, "PTR")[0])
        return ptr_record
    except (resolver.NoAnswer, resolver.NXDOMAIN, exception.SyntaxError):
        return ip


def main():
    parser = argparse.ArgumentParser(
        description="Returns DNS zone master for given domain for each server"
    )

    parser.add_argument(
        "-q",
        "--quiet",
        action="store_false",
        help="Only master ip will be returned",
    )

    parser.add_argument(
        "domains",
        nargs="?",
        type=str,
        help="List of domains to get zone master",
    )

    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Maximum verbosity",
    )

    args = parser.parse_args()
    verbosity_flag = args.quiet

    if args.domains:
        domain_list = args.domains.splitlines()
    else:
        domain_list = sys.stdin.read().strip().splitlines()

    results = [
        getDomainZoneMaster(
            domain,
            verbosity_flag=verbosity_flag,
            debug_flag=args.debug,
        )
        for domain in domain_list
    ]

    if verbosity_flag:
        for i, result in enumerate(results):
            domain = result["domain"]

            # Create the new answers structure
            results[i]["answers"] = [
                {
                    "host": answer["host"],
                    "zone_master": answer["stdout"],
                    "ptr": getPtr(answer["stdout"]),
                }
                for answer in result["answers"]
            ]
        ns_padding = 4
        extra_padding = 2
        domain_padding = (
            len(max([result["domain"] for result in results], key=len)) + extra_padding
        )

        ip_padding = (
            len(
                max(
                    [
                        answer["zone_master"]
                        for result in results
                        for answer in result["answers"]
                    ],
                    key=len,
                )
            )
            + extra_padding
        )

        ptr_padding = (
            len(
                max(
                    [
                        answer["ptr"]
                        for result in results
                        for answer in result["answers"]
                    ],
                    key=len,
                )
            )
            + extra_padding
        )

        print(
            f"{'Querying DNS servers about zone master...':^{ns_padding+ip_padding+ptr_padding+extra_padding}}"
        )

        print(
            f"{'NS':<{ns_padding}}|{'Domain':<{domain_padding}}|{'PTR':<{ptr_padding}}|{'IP':<{ip_padding}}"
        )

        for result in results:
            domain = result["domain"]
            for answer in result["answers"]:
                host = answer["host"].replace(".hoster.kz.", "")
                ip_value = answer["zone_master"]
                ptr_value = getPtr(ip_value)
                print(
                    f"{host:<{ns_padding}}|{domain:<{domain_padding}}|{ptr_value:<{ptr_padding}}|{ip_value:<{ip_padding}}"
                )
        sys.exit(0)
    else:
        return_value = 0
        for result in results:
            if (zone_master_count := len(result["zone_master"])) > 1:
                print(
                    f"[ERROR] Multiple zone masters [{zone_master_count}] for {result['domain']}"
                )
                return_value = 1
                print(f"{''.join(result['domain'])}|{''.join(result['zone_master'])}")
            else:
                print("".join(result["zone_master"]))
        sys.exit(return_value)


if __name__ == "__main__":
    main()
