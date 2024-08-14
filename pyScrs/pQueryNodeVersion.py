import async_ssh_executor as ase
import argparse
import pathlib
import datetime

SSH_USER = "maximg"
USER_HOME_DIR = pathlib.Path.home()
QUERY_RESULT_FILENAME = "pleskNodeVersionList"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="print actions of program",
    )

    args = parser.parse_args()

    statsFileName = (
        f"{QUERY_RESULT_FILENAME}{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    )
    statsDirName = "pkzStats"
    statsDirPath = f"{USER_HOME_DIR}/{statsDirName}"
    statsFilePath = f"{statsDirPath}/{statsFileName}"
    pathlib.Path(statsDirPath).mkdir(parents=True, exist_ok=True)
    print("Starting query...")

    results = ase.batch_ssh_command_result(
        "plesk",
        SSH_USER,
        "plesk ext nodejs --versions",
        verbose=args.verbose,
    )

    with open(statsFilePath, "w") as statsFile:
        for host in results:
            statsFile.write(f"{host["host"]} {host["stdout"]}\n")
    print(f"Saved in {statsFilePath}")
