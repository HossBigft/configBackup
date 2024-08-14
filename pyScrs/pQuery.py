import async_ssh_executor as ase
import pathlib
import datetime
import argparse


SSH_USER = "maximg"
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

    args = parser.parse_args()
    results = ase.batch_ssh_command_result(
        server_list="plesk", username=SSH_USER, command=args.command, verbose=True
    )
    results = [x for x in results if x["stdout"]]
    
    if not results:
        print(f"No results for query {args.command}")
        quit(1)

    statsFileName = (
        f"{args.fileName}{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    )
    statsDirPath = f"{pathlib.Path.home()}/{STATS_DIR_NAME}"
    statsFilePath = f"{statsDirPath}/{statsFileName}"

    pathlib.Path(statsDirPath).mkdir(parents=True, exist_ok=True)

    with open(statsFilePath, "w") as statsFile:
        for record in results:
            statsFile.write(f"{record['host']} {record['stdout']}\n")
    print(f"Saved in {statsFilePath}")
