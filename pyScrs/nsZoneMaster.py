import async_ssh_executor as ase
import argparse
import sys

SSH_USER = "root"
SERVER_LIST = "DNS"


def getDomainZoneMaster(
    domain_list: list, verbosity_flag=True, test_flag=False
):
    results = []
    for domain in domain_list:
        getZoneMasterCmd = f"cat /var/opt/isc/scls/isc-bind/zones/_default.nzf| grep {domain} | grep -Po '((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\\b){{4}}' | head -n1"
        dnsAnswers = []
        if test_flag:
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

    if verbosity_flag:
        for result in results:
            print(result["domain"])
            for answer in result["answers"]:
                print(f"{answer['host']}|{answer['stdout']}")
        sys.exit(0)
    else:
        for result in results:
            print("|".join(set([host["stdout"] for host in result["answers"]])))
        sys.exit(0)


def main():
    parser = argparse.ArgumentParser(
        description="Returns DNS zone master for given domain for each server"
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
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
    verbosity_flag = args.verbose
    if args.domains:
        domain_list = args.domains.splitlines()
    else:
        domain_list = sys.stdin.read().strip().splitlines()

    getDomainZoneMaster(
        domain_list=domain_list,
        verbosity_flag=verbosity_flag,
        test_flag=args.test
    )


if __name__ == "__main__":
    main()
