import async_ssh_executor as ase
import argparse

SSH_USER = "maximg"
SERVER_LIST = (
    "cloud-1.hoster.kz.",
    "aturbo-2.hoster.kz.",
    "apkz1.hoster.kz.",
    "apkz2.hoster.kz.",
    "apkz3.hoster.kz.",
    "apkz4.hoster.kz.",
    "apkz6.hoster.kz.",
    "apkz7.hoster.kz.",
    "pkz37.hoster.kz.",
    "pkz47.hoster.kz.",
    "pkz48.hoster.kz.",
    "pkz49.hoster.kz.",
    "pkz50.hoster.kz.",
    "pkz58.hoster.kz.",
    "cloud-2.hoster.kz",
    "nturbo-2.hoster.kz",
    "nturbo-1.hoster.kz",
    "pkz4.hoster.kz.",
    "pkz5.hoster.kz.",
    "pkz6.hoster.kz.",
    "pkz7.hoster.kz.",
    "pkz8.hoster.kz.",
    "pkz9.hoster.kz.",
    "pkz10.hoster.kz.",
    "pkz11.hoster.kz.",
    "pkz12.hoster.kz.",
    "pkz13.hoster.kz.",
    "pkz14.hoster.kz.",
    "pkz15.hoster.kz.",
    "pkz17.hoster.kz.",
    "pkz18.hoster.kz.",
    "pkz20.hoster.kz.",
    "pkz21.hoster.kz.",
    "pkz22.hoster.kz.",
    "pkz23.hoster.kz.",
    "pkz24.hoster.kz.",
    "pkz25.hoster.kz.",
    "pkz27.hoster.kz.",
    "pkz31.hoster.kz.",
    "pkz32.hoster.kz.",
    "pkz33.hoster.kz.",
    "pkz34.hoster.kz.",
    "pkz35.hoster.kz.",
    "pkz36.hoster.kz.",
    "pkz37.hoster.kz.",
    "pkz38.hoster.kz.",
    "pkz39.hoster.kz.",
    "pkz40.hoster.kz.",
    "pkz41.hoster.kz.",
    "pkz42.hoster.kz.",
    "pkz43.hoster.kz.",
    "pkz44.hoster.kz.",
    "pkz45.hoster.kz.",
    "pkz46.hoster.kz.",
    "pkz51.hoster.kz.",
    "pkz52.hoster.kz.",
    "pkz53.hoster.kz.",
    "pkz54.hoster.kz.",
    "pkz55.hoster.kz.",
    "pkz56.hoster.kz.",
    "pkz57.hoster.kz.",
    "pkz58.hoster.kz.",
    "pkz59.hoster.kz.",
    "pkz60.hoster.kz.",
    "pkz61.hoster.kz.",
    "pkz62.hoster.kz.",
    "pkz63.hoster.kz.",
    "pkz64.hoster.kz.",
    "pkz65.hoster.kz.",
    "pkz66.hoster.kz.",
    "pkz67.hoster.kz.",
    "pkz68.hoster.kz.",
    "cloud-3.hoster.kz.",
    "cloud-4.hoster.kz.",
    "cloud-5.hoster.kz.",
)


if __name__ == "__main__":
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

    args = parser.parse_args()
    v = vars(args)
    argsNumber = sum([1 for a in v.values() if a])
    if argsNumber == 1:
        args.verbose = args.name = args.id = args.domains = args.server = True

    results = ase.batch_ssh_command_result(
        SERVER_LIST,
        SSH_USER,
        f"plesk db -Ne \\\"SELECT CASE WHEN webspace_id = 0 THEN id ELSE webspace_id END AS result FROM domains WHERE name LIKE '{args.domainToFind}%';"
        + f"SELECT name FROM domains WHERE id=(SELECT CASE WHEN webspace_id = 0 THEN id ELSE webspace_id END AS result FROM domains WHERE name LIKE '{args.domainToFind}%');"
        + f"SELECT name FROM domains WHERE webspace_id=(SELECT CASE WHEN webspace_id = 0 THEN id ELSE webspace_id END AS result FROM domains WHERE name LIKE '{args.domainToFind}%')\\\"",
        verbose=args.verbose,
    )

    output_elements = []
    if args.server:
        if args.verbose:
            output_elements.append("Host:{hostname}")
        else:
            output_elements.append("{hostname}")

    if args.verbose and args.server:
        print(
            f"\nSubscription with {args.domainToFind} domain was found on following servers:"
        )

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

    results = [
        {
            "host": x["host"],
            "id": x["stdout"].strip().split("\n")[0],
            "name": x["stdout"].strip().split("\n")[1],
            "domains": x["stdout"].strip().split("\n")[2:],
        }
        for x in results
        if x["stdout"]
    ]
    if results:
        for record in results:
            print(
                "|".join(output_elements).format(
                    domaintoFind=args.domainToFind,
                    hostname=record["host"],
                    subscription_id=record["id"],
                    subscription_name=record["name"],
                )
            )
            if args.domains:
                if args.verbose:
                    print("Domains:")
                print(record["name"])
                for domain in record["domains"]:
                    print(domain)
            if len(results) > 1:
                print("-------")
    else:
        print(f"No servers was found with {args.domainToFind} domain")
