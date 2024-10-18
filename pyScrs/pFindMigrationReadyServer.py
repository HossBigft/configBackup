import ssh_async_executor as ase
import re
import pathlib
import datetime
import argparse
import os
from host_lists import PLESK_SERVER_LIST


class pkzServer:
    def __init__(
        self, name: str, totalSpace=0.0, usedSpace=0.0, pleskVersion=""
    ) -> None:
        self.name = name
        self.totalSpace = totalSpace
        self.usedSpace = usedSpace
        self.pleskVersion = pleskVersion

    def getUsedSpacePercent(self, spaceToAdd=0.0) -> float:
        if spaceToAdd == 0.0:
            return int(((self.usedSpace / self.totalSpace) * 10000 + 100 - 1) // 100)
        return int(
            (((self.usedSpace + spaceToAdd) / self.totalSpace) * 10000 + 100 - 1) // 100
        )

    def hasEnoughSpace(self, size: float) -> bool:
        return self.getUsedSpacePercent(size) <= 87

    def __versionCompare(self, v2: str) -> int:
        # This will split both the versions by '.'
        arr1 = self.pleskVersion.split(".")
        arr2 = v2.split(".")
        n = len(arr1)
        m = len(arr2)

        # converts to integer from string
        arr1 = [int(i) for i in arr1]
        arr2 = [int(i) for i in arr2]

        # compares which list is bigger and fills
        # smaller list with zero (for unequal delimiters)
        if n > m:
            for i in range(m, n):
                arr2.append(0)
        elif m > n:
            for i in range(n, m):
                arr1.append(0)

        # returns 1 if version 1 is bigger and -1 if
        # version 2 is bigger and 0 if equal
        for i in range(len(arr1)):
            if arr1[i] > arr2[i]:
                return 1
            elif arr2[i] > arr1[i]:
                return -1
        return 0

    def isCompatible(self, versionToCompare: str) -> bool:
        return self.__versionCompare(versionToCompare) in (1, 0)

    def getFreeSpace(self) -> int:
        return self.totalSpace - self.usedSpace

    def __str__(self) -> str:
        return f"Name: {self.name}\nTotal space: {self.totalSpace}\nUsed space:{self.usedSpace}\nPlesk Version:{self.pleskVersion}"


def __createFreeSpaceServerList(userHomeDirectory: str, fileName: str):
    statsFileName = f"{fileName}{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    statsDirName = "pkzStats"
    statsDirPath = f"{userHomeDirectory}/{statsDirName}"
    statsFilePath = f"{statsDirPath}/{statsFileName}"
    pathlib.Path(statsDirPath).mkdir(parents=True, exist_ok=True)
    print("Starting query...")
    serverSpaceData = ase.batch_ssh_command_result(
        server_list=PLESK_SERVER_LIST, command="df -BG", verbose=True
    )

    for record in serverSpaceData:
        if record["stdout"]:
            server = record["host"]
            currAnswer = record["stdout"].splitlines()
            currAnswer = [" ".join(line.split()) for line in currAnswer]

            currAnswer = re.search(
                r"(?:\S+\s+){5}\/var;|((?:\S+\s+){5}\/;)(?!.*\/var;)",
                ";".join(currAnswer),
            ).group(0)
            print(f"{server} answered {currAnswer}")
            record["stdout"] = currAnswer

    serverSpaceData = {
        record["host"]: record["stdout"]
        for record in serverSpaceData
        if record["stdout"]
    }

    print("Sorting by used space %")
    serverSpaceData = dict(
        sorted(serverSpaceData.items(), key=lambda item: int(item[1].split()[4][:-1]))
    )

    with open(statsFilePath, "w") as statsFile:
        for host, line in serverSpaceData.items():
            statsFile.write(f"{host} {line}\n")
    print(f"Saved in {statsFilePath}")


def __createServerVersionList(userHomeDirectory: str, fileName: str):
    statsFileName = f"{fileName}{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    statsDirName = "pkzStats"
    statsDirPath = f"{userHomeDirectory}/{statsDirName}"
    statsFilePath = f"{statsDirPath}/{statsFileName}"
    pathlib.Path(statsDirPath).mkdir(parents=True, exist_ok=True)
    print("Starting query...")
    serverVersionData = ase.batch_ssh_command_result(
        server_list=PLESK_SERVER_LIST, command="plesk -v", verbose=True
    )

    for record in serverVersionData:
        if record["stdout"]:
            server = record["host"]
            currAnswer = record["stdout"].splitlines()
            currAnswer = [" ".join(line.split()) for line in currAnswer]
            currAnswer = "".join(filter(lambda s: re.search(r"Plesk.*", s), currAnswer))
            print(f"{server} answered {currAnswer}")
            record["stdout"] = currAnswer

    serverVersionData = {
        record["host"]: record["stdout"]
        for record in serverVersionData
        if record["stdout"]
    }
    serverVersionData = {
        key: re.search(r"\d+(\.\d+)+", value).group(0)
        for key, value in serverVersionData.items()
    }

    print("Sorting by Plesk version")
    serverVersionData = dict(
        sorted(serverVersionData.items(), key=lambda item: item[1])
    )
    with open(statsFilePath, "w") as statsFile:
        for host, line in serverVersionData.items():
            statsFile.write(f"{host} {line}\n")
    print(f"Saved in {statsFilePath}")


class InsufficientSpaceError(Exception):
    def __init__(self, siteSize: float) -> None:
        super().__init__(
            f"No servers have enough free space to fit the size: {round(siteSize)} Gb"
        )


class NoCompatiblePleskVersionError(Exception):
    def __init__(self, targetVersion: float) -> None:
        super().__init__(
            f"No servers are compatible with target version: {targetVersion}"
        )


def regex_type(pattern: str | re.Pattern):
    def closure_check_regex(arg_value):
        if not re.match(pattern, arg_value):
            raise argparse.ArgumentTypeError(
                f"Provided value doesn't match pattern {pattern}"
            )
        return arg_value

    return closure_check_regex


USER_HOME_DIR = pathlib.Path.home()
SERVER_FREE_SPACE_FILENAME = "pleskAvalSpaceList"
SERVER_VERSION_FILENAME = "pleskServerVersionList"

parser = argparse.ArgumentParser()

parser.add_argument(
    "targetVersion",
    type=regex_type(r"\d+(\.\d+)+"),
    help="site's host Plesk version",
    metavar="target Plesk version",
)

parser.add_argument(
    "siteSize",
    type=regex_type(r"^[+-]?([0-9]+([.][0-9]*)?|[.][0-9]+)$"),
    help="size of site to migrate",
    metavar="size",
)

parser.add_argument(
    "-r",
    "--refresh",
    action="store_false",
    help="run query again instead of using existing result",
)

args = parser.parse_args()
siteSize = float(args.siteSize)
serverData = {}
versionDataPath: str
spaceDataPath: str


if (
    not any(
        pathlib.Path(f"{USER_HOME_DIR}/pkzStats").glob(
            f"{SERVER_VERSION_FILENAME}{datetime.datetime.now().strftime('%Y%m%d')}*.txt"
        )
    )
    or not args.refresh
):
    print("No relevant file with server versions was found")
    __createServerVersionList(USER_HOME_DIR, SERVER_VERSION_FILENAME)
    versionDataPath = max(
        pathlib.Path(f"{USER_HOME_DIR}/pkzStats").glob(
            f"{SERVER_VERSION_FILENAME}{datetime.datetime.now().strftime('%Y%m%d')}*.txt"
        ),
        key=os.path.getctime,
    )
else:
    versionDataPath = max(
        pathlib.Path(f"{USER_HOME_DIR}/pkzStats").glob(
            f"{SERVER_VERSION_FILENAME}{datetime.datetime.now().strftime('%Y%m%d')}*.txt"
        ),
        key=os.path.getctime,
    )
#    print(f"Found version datafile: {versionDataPath}")

with open(versionDataPath) as v:
    for splitLines in v:
        splitLines = splitLines.split(" ")
        currServerName = re.search(r"^([^.])+", splitLines[0]).group(0)
        currVersion = splitLines[1].strip("\n")
        currServer = pkzServer(currServerName, pleskVersion=currVersion)
        if currServer.isCompatible(args.targetVersion):
            serverData[currServerName] = currServer
if len(serverData) == 0:
    raise NoCompatiblePleskVersionError(args.targetVersion)

if (
    not any(
        pathlib.Path(f"{USER_HOME_DIR}/pkzStats").glob(
            f"{SERVER_FREE_SPACE_FILENAME}{datetime.datetime.now().strftime('%Y%m%d')}*.txt"
        )
    )
    or not args.refresh
):
    print("No relevant file with server space was found")
    __createFreeSpaceServerList(USER_HOME_DIR, SERVER_FREE_SPACE_FILENAME)
    spaceDataPath = max(
        pathlib.Path(f"{USER_HOME_DIR}/pkzStats").glob(
            f"{SERVER_FREE_SPACE_FILENAME}{datetime.datetime.now().strftime('%Y%m%d')}*.txt"
        ),
        key=os.path.getctime,
    )
else:
    spaceDataPath = max(
        pathlib.Path(f"{USER_HOME_DIR}/pkzStats").glob(
            f"{SERVER_FREE_SPACE_FILENAME}{datetime.datetime.now().strftime('%Y%m%d')}*.txt"
        ),
        key=os.path.getctime,
    )
#    print(f"Found space datafile: {spaceDataPath}")

with open(spaceDataPath) as f:
    for line in f:
        splitLines = line.replace("\n", "").split(" ", 1)
        currServerName = re.search(r"^([^.])+", splitLines[0]).group(0)
        currServerData = " ".join(splitLines[1].split()).replace("G", "").split(" ")
        currTotalSpace, currUsedSpace = int(currServerData[1]), int(currServerData[2])
        currServer = pkzServer(currServerName, currTotalSpace, currUsedSpace)
        if currServer.hasEnoughSpace(siteSize) and currServer.name in serverData.keys():
            currServer.pleskVersion = serverData[currServer.name].pleskVersion
            serverData[currServer.name] = currServer
        elif currServer.name in serverData.keys():
            del serverData[currServer.name]
if len(serverData) == 0:
    raise InsufficientSpaceError(siteSize)

serverData = dict(
    sorted(
        serverData.items(), key=lambda item: round(item[1].getFreeSpace() - siteSize)
    )
)
print("server | Total | Used | Free | Used% | Host version >= Target version")
for server, data in serverData.items():
    print(
        f"{server} | {data.totalSpace} GB | {data.usedSpace}=>{round(data.usedSpace+siteSize)} Gb | {data.getFreeSpace()}=>{round(data.getFreeSpace()-siteSize)} Gb | {data.getUsedSpacePercent()}=>{data.getUsedSpacePercent(siteSize)}% | {data.pleskVersion}>={args.targetVersion}"
    )
