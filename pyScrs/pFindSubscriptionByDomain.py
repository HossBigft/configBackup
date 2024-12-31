import argparse
from ssh_plesk_subscription_info_retriever import query_domain_info


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
            # Prepare the output elements based on the flags
            output_elements = []
            if args.name:
                output_elements.append("{subscription_name}")
            if args.id:
                output_elements.append("{subscription_id}")
            if args.server:
                output_elements.append("{hostname}")
            if args.user:
                output_elements.append("{username} ({userlogin})")

            # Print the formatted output if any of the flags are set
            if output_elements:
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

            # Print domains if the 'domains' flag is set
            if args.domains:
                if args.verbose:
                    print("Domains:")
                print(record["name"])  # Print the main subscription name
                for domain in record["domains"]:
                    print(
                        domain["domain"]
                    )  # Each domain is a dictionary, so access 'domain' key

            # Print a separator if there are multiple results and verbose is enabled
            if len(results) > 1 and args.verbose:
                print("-------")
    else:
        print(f"No servers were found with {args.domainToFind} domain")


if __name__ == "__main__":
    main()
