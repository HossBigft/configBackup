import async_ssh_executor as ase
import argparse
import sys
from dns import resolver, reversename
from beautifultable import BeautifulTable

SSH_USER = "root"
SERVER_LIST = "DNS"
DNS_HOSTING_HOSTNAME = "dns.hoster.kz."

def getPtr(ip:str):
    try:
        addr_record = reversename.from_address(ip)
        ptr_record = str(resolver.resolve(addr_record, "PTR")[0])
        return(ptr_record)
    except (resolver.NoAnswer, resolver.NXDOMAIN):
        return ip

def getDomainZoneMaster(domain_name, verbosity_flag=True, test_flag=False):
    getZoneMasterCmd = f"cat /var/opt/isc/scls/isc-bind/zones/_default.nzf| grep {''.join(domain_name)} | grep -Po '((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\\b){{4}}' | head -n1"
    dnsAnswers = []
    dnsAnswers = ase.batch_ssh_command_result(
        server_list=SERVER_LIST,
        username=SSH_USER,
        command=getZoneMasterCmd,
        verbose=verbosity_flag,
        test=test_flag,
    )
    if verbosity_flag:
        return {"domain": f"{domain_name}", "answers": dnsAnswers}

    unique_zone_masters = list(set(answer["stdout"] for answer in dnsAnswers))
    return {
        "domain": domain_name,
        "zone_master": unique_zone_masters,
    }


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
        "-t",
        "--test",
        action="store_true",
        help="query will run on test hosts",
    )

    parser.add_argument(
        "domains",
        nargs="?",
        type=str,
        help="List of domains to get zone master",
    )

    args = parser.parse_args()
    verbosity_flag = args.quiet

    if args.domains:
        domain_list = args.domains.splitlines()
    else:
        domain_list = sys.stdin.read().strip().splitlines()

    results = [
        getDomainZoneMaster(domain, verbosity_flag=verbosity_flag, test_flag=args.test)
        for domain in domain_list
    ]

    if verbosity_flag:
        table = BeautifulTable()
        table.columns.header = ["Domain", "Nameservers: ns1.hoster.kz, ns2.hoster.kz, ns3.hoster.kz"]
        for result in results:
            table_row = []
            dns_row = []
            ptr_row = []
            table_row.append(result["domain"])
            
            for answer in result["answers"]:
                dns_row.append(answer["stdout"])
                ptr_row.append(getPtr(answer["stdout"]))
                
            dns_combined = ", ".join(dns_row)
            ptr_combined = ", ".join(ptr_row)
            
            table_row.append(ptr_combined+"\n"+dns_combined)
            table.rows.append(table_row)

        print(table)
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
