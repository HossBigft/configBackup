import pyScrs.ssh_async_executor as ase
import argparse
from host_lists import PLESK_SERVER_LIST


def build_query(domain_to_find: str) -> str:
    return (
        f"SELECT CASE WHEN webspace_id = 0 THEN id ELSE webspace_id END AS result "
        f"FROM domains WHERE name LIKE '{domain_to_find}'; "
        f"SELECT name FROM domains WHERE id=(SELECT CASE WHEN webspace_id = 0 THEN id ELSE webspace_id END AS result FROM domains WHERE name LIKE '{domain_to_find}'); "
        f"SELECT pname, login FROM clients WHERE id=(SELECT cl_id FROM domains WHERE name LIKE '{domain_to_find}'); "
        f"SELECT name FROM domains WHERE webspace_id=(SELECT CASE WHEN webspace_id = 0 THEN id ELSE webspace_id END AS result FROM domains WHERE name LIKE '{domain_to_find}');"
    )


def parse_answer(answer) -> dict:
    stdout_lines = answer["stdout"].strip().split("\n")
    return {
        "host": answer["host"],
        "id": stdout_lines[0],
        "name": stdout_lines[1],
        "username": stdout_lines[2].split("\t")[0],
        "userlogin": stdout_lines[2].split("\t")[1],
        "domains": stdout_lines[3:],
    }


def query_domain_info(domain_to_find: str, verbose_flag=True, partial_search=False):
    query = (
        build_query(domain_to_find)
        if not partial_search
        else build_query(domain_to_find + "%")
    )

    answers = ase.batch_ssh_command_result(
        PLESK_SERVER_LIST,
        f'plesk db -Ne \\"{query}\\"',
        verbose=verbose_flag,
    )

    results = [parse_answer(answer) for answer in answers if answer["stdout"]]
    return results


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "domainToFind",
        type=str,
        help="domain that will be searched on Plesk servers",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="print actions of program",
    )
    parser.add_argument(
        "-n",
        "--name",
        action="store_true",
        help="print subscription name",
    )
    parser.add_argument(
        "-i",
        "--id",
        action="store_true",
        help="print subscription id",
    )
    parser.add_argument(
        "-d",
        "--domains",
        action="store_true",
        help="print subscription domains",
    )
    parser.add_argument(
        "-s",
        "--server",
        action="store_true",
        help="print server hostname",
    )
    parser.add_argument(
        "-u",
        "--user",
        action="store_true",
        help="print user name and login",
    )
    parser.add_argument(
        "-p",
        "--partial",
        action="store_true",
        help="search by part of domain name",
    )

    args = parser.parse_args()
    v = vars(args)
    argsNumber = sum([1 for a in v.values() if a])
    if argsNumber == 1:
        args.verbose = args.name = args.id = args.domains = args.server = args.user = (
            args.partial
        ) = True

    output_elements = []
    if args.server:
        if args.verbose:
            output_elements.append("Host:{hostname}")
        else:
            output_elements.append("{hostname}")

    if args.id:
        if args.verbose:
            output_elements.append("Subscription ID:{subscription_id}")
        elif args.id:
            output_elements.append("{subscription_id}")

    if args.name:
        if args.verbose:
            output_elements.append("Subscription Name:{subscription_name}")
        elif args.name:
            output_elements.append("{subscription_name}")

    if args.user:
        if args.verbose:
            output_elements[:] = [
                *output_elements,
                *["Username:{username}", "Userlogin:{userlogin}"],
            ]
        else:
            output_elements[:] = [*output_elements, *["{username}", "{userlogin}"]]
    if args.partial:
        results = query_domain_info(
            args.domainToFind, verbose_flag=args.verbose, partial_search=True
        )
    else:
        results = query_domain_info(args.domainToFind, verbose_flag=args.verbose)

    if results:
        if args.verbose and args.server:
            print(
                f"\nSubscription with {args.domainToFind} domain was found on following servers[{len(results)}]:"
            )
        for record in results:
            if args.name or args.id or args.server or args.user:
                print(
                    "|".join(output_elements).format(
                        domaintoFind=args.domainToFind,
                        hostname=record["host"],
                        subscription_id=record["id"],
                        subscription_name=record["name"],
                        username=record["username"],
                        userlogin=record["userlogin"],
                    )
                )
            if args.domains:
                if args.verbose:
                    print("Domains:")
                print(record["name"])
                for domain in record["domains"]:
                    print(domain)
            if len(results) > 1 and args.verbose:
                print("-------")
    else:
        print(f"No servers was found with {args.domainToFind} domain")


if __name__ == "__main__":
    main()
