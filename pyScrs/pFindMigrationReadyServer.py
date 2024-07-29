import subprocess
import re
import pathlib
import shlex
import datetime
import argparse


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


def __send_command_to_servers(cmd: str, sshUser: str, serverList: list) -> dict:
    serverAnswers = {}
    for host in serverList:
        sshCommand = f"ssh {sshUser}@{host} {cmd}"
        print(f"Querying {host} with: {cmd}")
        sshOutput = subprocess.run(
            shlex.split(sshCommand), capture_output=True, text=True
        )
        serverAnswers[host] = sshOutput.stdout
    return serverAnswers


def __createFreeSpaceServerList(sshUser: str, userHomeDirectory: str, fileName: str):
    statsFileName = f"{fileName}{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    statsDirName = "pkzStats"
    statsDirPath = f"{USER_HOME_DIR}/{statsDirName}"
    statsFilePath = f"{statsDirPath}/{statsFileName}"
    pathlib.Path(statsDirPath).mkdir(parents=True, exist_ok=True)
    print("Starting query...")
    serverSpaceData = __send_command_to_servers("df -BG", sshUser, SERVER_LIST)

    for server, answer in serverSpaceData.items():
        currAnswer = answer.splitlines()
        currAnswer = [" ".join(line.split()) for line in currAnswer]
        currAnswer = "".join(
            filter(
                lambda s: re.fullmatch(
                    r"(?:\S+\s+){5}/var;|((?:\S+\s+){5}/)(?!.*/var)", s
                ),
                currAnswer,
            )
        )
        print(f"{server} answered {currAnswer}")
        serverSpaceData[server] = currAnswer

    print("Sorting by used space %")
    serverSpaceData = dict(
        sorted(serverSpaceData.items(), key=lambda item: int(item[1].split()[4][:-1]))
    )

    with open(statsFilePath, "w") as statsFile:
        for host, line in serverSpaceData.items():
            statsFile.write(f"{host} {line}\n")
    print(f"Saved in {statsFilePath}")


def __createServerVersionList(user: str, userHomeDirectory: str, fileName: str):
    statsFileName = f"{fileName}{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    statsDirName = "pkzStats"
    statsDirPath = f"{USER_HOME_DIR}/{statsDirName}"
    statsFilePath = f"{statsDirPath}/{statsFileName}"
    pathlib.Path(statsDirPath).mkdir(parents=True, exist_ok=True)
    print("Starting query...")
    serverVersionData = __send_command_to_servers("plesk -v", SSH_USER, SERVER_LIST)

    for server, answer in serverVersionData.items():
        currAnswer = answer.splitlines()
        currAnswer = [" ".join(line.split()) for line in currAnswer]
        currAnswer = "".join(filter(lambda s: re.search(r"Plesk.*", s), currAnswer))
        print(f"{server} answered {currAnswer}")
        serverVersionData[server] = currAnswer

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


SSH_USER = "maximg"
USER_HOME_DIR = pathlib.Path.home()
SERVER_FREE_SPACE_FILENAME = "pleskAvalSpaceList"
SERVER_VERSION_FILENAME = "pleskServerVersionList"
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

args = parser.parse_args()
siteSize = float(args.siteSize)
serverData = {}
versionDataPath: str
spaceDataPath: str


if not any(
    pathlib.Path(f"{USER_HOME_DIR}/pkzStats").glob(
        f"{SERVER_VERSION_FILENAME}{datetime.datetime.now().strftime('%Y%m%d')}*.txt"
    )
):
    print("No relevant file with server versions was found")
    __createServerVersionList(SSH_USER, USER_HOME_DIR, SERVER_VERSION_FILENAME)
    versionDataPath = list(
    pathlib.Path(f"{USER_HOME_DIR}/pkzStats").glob(
        f"{SERVER_VERSION_FILENAME}{datetime.datetime.now().strftime('%Y%m%d')}*.txt"
    )
)[-1]
else:
    versionDataPath = list(
        pathlib.Path(f"{USER_HOME_DIR}/pkzStats").glob(
            f"{SERVER_VERSION_FILENAME}{datetime.datetime.now().strftime('%Y%m%d')}*.txt"
        )
    )[-1]
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

if not any(
    pathlib.Path(f"{USER_HOME_DIR}/pkzStats").glob(
        f"{SERVER_FREE_SPACE_FILENAME}{datetime.datetime.now().strftime('%Y%m%d')}*.txt"
    )
):
    print("No relevant file with server space was found")
    __createFreeSpaceServerList(SSH_USER, USER_HOME_DIR, SERVER_FREE_SPACE_FILENAME)
    spaceDataPath = list(
        pathlib.Path(f"{USER_HOME_DIR}/pkzStats").glob(
            f"{SERVER_FREE_SPACE_FILENAME}{datetime.datetime.now().strftime('%Y%m%d')}*.txt"
        )
    )[-1]
else:
    spaceDataPath = list(
        pathlib.Path(f"{USER_HOME_DIR}/pkzStats").glob(
            f"{SERVER_FREE_SPACE_FILENAME}{datetime.datetime.now().strftime('%Y%m%d')}*.txt"
        )
    )[-1]
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
        sorted(serverData.items(), key=lambda item: item[1].getUsedSpacePercent(), reverse=True)
    )
print("server | Total | Free | Used%| Host version >= Target version")
for server, data in serverData.items():
    print(
        f"{server} | {data.totalSpace}=>{round(data.totalSpace+siteSize)} Gb | {data.getFreeSpace()}=>{round(data.getFreeSpace()-siteSize)} Gb | {data.getUsedSpacePercent()}=>{data.getUsedSpacePercent(siteSize)}% | {data.pleskVersion}>={args.targetVersion}"
    )
