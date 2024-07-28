import subprocess, re, pathlib, shlex, datetime, argparse
from dataclasses import dataclass
from collections import namedtuple


class pkzServer:

    def __init__(
        self, name: str, totalSpace: int, usedSpace: int, pleskVersion=""
    ) -> None:
        self.name = name
        self.totalSpace = totalSpace
        self.usedSpace = usedSpace
        self.pleskVersion = pleskVersion

    def getUsedSpacePercent(self) -> int:
        return int(((self.usedSpace / self.totalSpace) * 10000 + 100 - 1) // 100)

    def getUsedSpacePercent(self, spaceToAdd: float) -> int:
        return int(
            (((self.usedSpace + spaceToAdd) / self.totalSpace) * 10000 + 100 - 1) // 100
        )

    def hasEnoughSpace(self, size: float) -> bool:
        return self.getUsedSpacePercent(size) <= 87

    def __versionCompare(v1, v2) -> int:
        # This will split both the versions by '.'
        arr1 = v1.split(".")
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
        return self.__versionCompare(self.pleskVersion, versionToCompare) in (-1, 0)


def __send_command_to_servers(cmd: str, sshUser: str, serverList: list) -> dict:
    serverAnswers = {}
    for host in serverList[:5]:
        sshCommand = f"ssh {sshUser}@{host} {cmd}"
        print(f"Querying {host} with {cmd}")
        sshOutput = subprocess.run(
            shlex.split(sshCommand), capture_output=True, text=True
        )
        serverAnswers[host] = sshOutput.stdout
    return serverAnswers


def __filter_server_answer_by_regex(serverAnswers: dict, pattern: str) -> dict:
    filteredAnswers = {}
    for server, answer in serverAnswers.items():
        currAnswer = answer.splitlines()
        currAnswer = [" ".join(line.split()) for line in currAnswer]
        currAnswer = "".join(
            filter(lambda s: re.fullmatch(rf"{pattern}", s), currAnswer)
        )
        print(f"{server} answered {currAnswer}")
        filteredAnswers[server] = currAnswer
    return filteredAnswers


def __createFreeSpaceServerList(sshUser: str, userHomeDirectory: str, fileName: str):
    statsFileName = f"{fileName}{datetime.datetime.now().strftime('%Y%m%d_%H%M')}"
    statsDirName = "pkzStats"
    statsDirPath = f"{USER_HOME_DIR}/{statsDirName}"
    statsFilePath = f"{statsDirPath}/{statsFileName}"
    pathlib.Path(statsDirPath).mkdir(parents=True, exist_ok=True)

    serverSpaceData = __send_command_to_servers("df -BG", sshUser, SERVER_LIST)
    serverSpaceData = __filter_server_answer_by_regex(
        serverSpaceData, "(?:\S+\s+){5}/var;|((?:\S+\s+){5}/)(?!.*/var)"
    )

    print("Sorting by used space %")
    serverSpaceData = sorted(
        serverSpaceData.items(), key=lambda item: int(item[1].split()[4][:-1])
    )

    with open(statsFilePath, "w") as statsFile:
        for host, line in serverSpaceData.items():
            statsFile.write(f"{host}; {line};\n")
    print(f"Saved in {statsFilePath}")


def __createServerVersionList(user: str, userHomeDirectory: str, fileName: str):
    statsFileName = f"{fileName}{datetime.datetime.now().strftime('%Y%m%d_%H%M')}"

    statsDirName = "pkzStats"
    statsDirPath = f"{USER_HOME_DIR}/{statsDirName}"
    statsFilePath = f"{statsDirPath}/{statsFileName}"
    pathlib.Path(statsDirPath).mkdir(parents=True, exist_ok=True)

    serverVersionData = __send_command_to_servers("plesk -v", SSH_USER, SERVER_LIST)
    serverSpaceData = __filter_server_answer_by_regex(serverSpaceData, "Plesk.*")

    print("Sorting by Plesk Version")
    serverVersionData = sorted(serverVersionData.items(), key=lambda item: int(item[1]))

    with open(statsFilePath, "w") as statsFile:
        for host, line in serverVersionData.items():
            statsFile.write(f"{host}; {line};\n")
    print(f"Saved in {statsFilePath}")


class InsufficientSpaceError(Exception):
    def __init__(self, siteSize: float) -> None:
        super().__init__(
            f"No servers have enough free space to fit the size:{siteSize}gb"
        )


class NoCompatiblePleskVersionError(Exception):
    def __init__(self, targetVersion: float) -> None:
        super().__init__(
            f"No servers are compatible with target version:{targetVersion}"
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
    " target Plesk version",
    dest="targetVersion",
    required=True,
    type=regex_type(r"\d+(\.\d+)+"),
    help="site's host Plesk version",
    metavar="v",
)

parser.add_argument(
    "size",
    dest="siteSize",
    type=regex_type(r"^[+-]?([0-9]+([.][0-9]*)?|[.][0-9]+)$"),
    help="size of site to migrate",
    metavar="s",
)

args = parser.parse_args()

serverData: dict[str, pkzServer]
versionDataPath: str
spaceDataPath: str

if not any(
    pathlib.Path(f"{USER_HOME_DIR}/pkzStats").glob(
        f"{SERVER_FREE_SPACE_FILENAME}{datetime.datetime.now().strftime('%Y%m%d')}*"
    )
):
    print("No relevant file with server space was found")
    __createFreeSpaceServerList(SSH_USER, USER_HOME_DIR, SERVER_FREE_SPACE_FILENAME)
    spaceDataPath = list(
        pathlib.Path(f"{USER_HOME_DIR}/pkzStats").glob("pleskAvailableSpace*")
    )[-1]
elif any(
    pathlib.Path(f"{USER_HOME_DIR}/pkzStats").glob(
        f"{SERVER_VERSION_FILENAME}{datetime.datetime.now().strftime('%Y%m%d')}*"
    )
):
    print("No relevant file with server versions was found")
    __createServerVersionList()(SSH_USER, USER_HOME_DIR, SERVER_FREE_SPACE_FILENAME)
    versionDataPath = list(
        pathlib.Path(f"{USER_HOME_DIR}/pkzStats").glob("pleskVersion*")
    )[-1]


with open(spaceDataPath) as f:
    for line in f:
        line = line.replace("\n", "").replace("G", "").split(" ", 1)
        currServerName = re.search(r"^([^.])+", line[0]).group(0)
        currServerData = line[1].split(" ")
        currTotalSpace, currUsedSpace = int(currServerData[1]), int(currServerData[2])
        currServer = pkzServer(currServerName, currTotalSpace, currUsedSpace)
        if currServer.hasEnoughSpace(args.siteSize):
            serverData[currServer.name] = currServer
if len(serverData) == 0:
    raise InsufficientSpaceError(args.siteSize)


with open(versionDataPath) as v:
    for line in v:
        currVersion = line.replace("\n", "")
        currServerName = re.search(r"^([^.])+", line[0]).group(0)
        serverData[currServerName].pleskVersion = currVersion
        if not serverData[currServerName].isCompatible(args.targetVersion):
            del serverData[currServerName]
if len(serverData) == 0:
    raise NoCompatiblePleskVersionError(args.targetVersion)


print("server|Total|Free|Used%|Host version >= Target version")
for server, data in serverData.items():
    print(
        f"{server}|{data.totalSpace}=>{data.totalSpace+args.siteSize}|{data.free}=>{data.free-args.siteSize}|{data.getUsedPercent()}%=>{data.getUsedPercent(args.siteSize)}|{data.pleskVersion}>={args.targetVersion}"
    )
