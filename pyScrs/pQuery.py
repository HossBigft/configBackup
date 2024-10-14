import async_ssh_executor as ase
import pathlib
import datetime
import argparse
from host_lists import PLESK_SERVER_LIST, TEST_SERVER_LIST


STATS_DIR_NAME = "pkzStats"
USER_HOME_DIR = pathlib.Path.home()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "filename",
        type=str,
        help="the name of the text file in which the server responses will be stored",
    )

    parser.add_argument(
        "command",
        type=str,
        help="command that will be sent to Plesk servers",
    )

    parser.add_argument(
        "-o",
        "--oneline",
        action="store_true",
        help="output will we written in singleline",
    )

    parser.add_argument(
        "-t",
        "--test",
        action="store_true",
        help="query will run on test hosts",
    )

    args = parser.parse_args()
    if args.test:
        results = ase.batch_ssh_command_result(
            server_list=TEST_SERVER_LIST,
            command=args.command,
            verbose=True,
        )
    else:
        results = ase.batch_ssh_command_result(
            server_list=PLESK_SERVER_LIST, command=args.command, verbose=True
        )
    if args.oneline:
        results = [
            {"host": x["host"], "stdout": ";".join(x["stdout"].split())}
            for x in results
            if x["stdout"]
        ]
    else:
        results = [
            {"host": x["host"], "stdout": x["stdout"], "stderr": x["stderr"]}
            for x in results
            if x["stdout"] or x["stderr"]
        ]

    if not results:
        print(f"No results for query {args.command}")
        quit(1)

    if args.oneline:
        statsFileName = f"{args.filename}_oneline{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    else:
        statsFileName = (
            f"{args.filename}{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.txt"
        )
    statsDirPath = f"{pathlib.Path.home()}/{STATS_DIR_NAME}"
    statsFilePath = f"{statsDirPath}/{statsFileName}"

    pathlib.Path(statsDirPath).mkdir(parents=True, exist_ok=True)
    with open(statsFilePath, "w") as statsFile:
        for record in results:
            if record["stdout"] and not record["stderr"]:
                statsFile.write(f"[0]{record['host']}|{record['stdout']}\n")
            elif record["stderr"] and not record["stdout"]:
                statsFile.write(f"[1]{record['host']}|{record['stderr']}\n")
            elif record["stdout"] and record["stderr"]:
                statsFile.write(
                    f"[01]{record['host']}|{record['stdout']}||{record['stderr']}\n"
                )
    print(f"Saved in {statsFilePath}")
