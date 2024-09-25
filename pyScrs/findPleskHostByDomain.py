import argparse
from dns import resolver, reversename
import sys
import nsZoneMaster
import pFindSubscriptionByDomain as pfind


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
    print(f"Starting host resolution for {domain} using A record.")
    try:
        a_record = "".join([ipval.to_text() for ipval in resolver.resolve(domain, "A")])
        try:
            addr_record = reversename.from_address(a_record)
            ptr_record = str(resolver.resolve(addr_record, "PTR")[0])
            if "hoster.kz" in ptr_record:
                print(ptr_record, end="")
                sys.exit(0)
            else:
                print(f"No substring 'hoster.kz' in {ptr_record}.")
        except (resolver.NoAnswer, resolver.NXDOMAIN):
            print(f"[FAIL] PTR record not found for {a_record}. PTR lookup failed.")
    except (resolver.NoAnswer, resolver.NXDOMAIN):
        print(f"[FAIL] A record not found for {domain}.")

    print(f"Attempting to resolve host for {domain} using MX record.")
    try:
        mx_record = "".join(
            [ipval.to_text() for ipval in resolver.resolve(domain, "MX")]
        ).split(" ")[1]
        a_record = "".join(
            [ipval.to_text() for ipval in resolver.resolve(mx_record, "A")]
        )
        try:
            addr_record = reversename.from_address(a_record)
            ptr_record = str(resolver.resolve(addr_record, "PTR")[0])
            if "hoster.kz" in ptr_record:
                print(ptr_record, end="")
                sys.exit(0)
            else:
                print(f"No substring 'hoster.kz' in {ptr_record}.")
        except (resolver.NoAnswer, resolver.NXDOMAIN):
            print(f"[FAIL] PTR record not found for {mx_record}. PTR lookup failed.")
    except (resolver.NoAnswer, resolver.NXDOMAIN):
        print(f"[FAIL] MX record not found for {domain}.")

    print(f"Attempting to resolve host for {domain} using DNS zone master.")
    if zone_master_a_record := "".join(
        nsZoneMaster.getDomainZoneMaster(domain, verbosity_flag=False)
    ):
        try:
            addr_record = reversename.from_address(zone_master_a_record)
            ptr_record = str(resolver.resolve(addr_record, "PTR")[0])
            if "hoster.kz" in ptr_record:
                print(ptr_record, end="")
                sys.exit(0)
            else:
                print(f"No substring 'hoster.kz' in {ptr_record}.")
        except (resolver.NoAnswer, resolver.NXDOMAIN):
            print(f"[FAIL] PTR record not found for {a_record}. PTR lookup failed.")
    else:
        print(f"[FAIL] Zone master not found for {domain}.")

    print(f"Attempting to find host {domain} by querying servers.")
    if answers:= pfind.query_domain_info(domain, verbose_flag=False):
        for answer in answers:
            print(answer["host"])
    else:
        print("[ERROR] Host for {domain} not found.")
if __name__ == "__main__":
    main()
