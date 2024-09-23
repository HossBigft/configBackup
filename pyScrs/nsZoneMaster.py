import async_ssh_executor as ase
import argparse
import sys

SSH_USER = "root"
SERVER_LIST = "DNS"


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

    results = []
    for domain in domain_list:
        getZoneMasterCmd = f"cat /var/opt/isc/scls/isc-bind/zones/_default.nzf| grep {domain} | grep -Po '((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\\b){{4}}' | head -n1"
        dnsAnswers = []
        if args.test:
            dnsAnswers = ase.batch_ssh_command_result(
                server_list=SERVER_LIST,
                username=SSH_USER,
                command=getZoneMasterCmd,
                verbose=verbosity_flag,
                test=True,
            )

        else:
            dnsAnswers = ase.batch_ssh_command_result(
                server_list=SERVER_LIST,
                username=SSH_USER,
                command=getZoneMasterCmd,
                verbose=verbosity_flag,
            )
        results.append({"domain": f"{domain}", "answers": dnsAnswers})
    
    for result in results:
        print(result["domain"])
        for answer in result["answers"]:
            print(f"{answer['host']}|{answer['stdout']}")

if __name__ == "__main__":
    main()
