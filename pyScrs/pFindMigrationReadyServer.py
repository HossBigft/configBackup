import subprocess, re, pathlib, shlex, datetime
from dataclasses import dataclass
from collections import namedtuple

sshUser = "maximg"
userHomeDir = pathlib.Path.home()
avalSpaceFileName = "pleskAvalSpaceList"
serverVersionFileName = "pleskServerVersionList"


@dataclass
class pkzServer:
    name: str
    mainFileSystem: str
    totalSpace: int
    usedSpace: int
    freeSpace: int
    pleskVersion: str


def __send_command_to_pkz_servers(cmd: str, sshUser: str) -> dict:
    hosts = (
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
    serverAnswers = {}
    for host in hosts[:5]:
        sshCommand = f"ssh {sshUser}@{host} {cmd}"
        print(f"Querying {host} with {cmd}")
        sshOutput = subprocess.run(
            shlex.split(sshCommand), capture_output=True, text=True
        )
        print(f"{host} answered {sshOutput.stdout}")
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
        filteredAnswers[server] = currAnswer
    return filteredAnswers


def __createFreeSpaceServerList(sshUser: str, userHomeDirectory: str, fileName: str):
    statsFileName = f"{fileName}{datetime.datetime.now().strftime('%Y%m%d_%H%M')}"
    fileDirName = "pkzStats"
    statsDirPath = f"{userHomeDir}/{fileDirName}"
    statsFilePath = f"{statsDirPath}/{statsFileName}"
    pathlib.Path(statsDirPath).mkdir(parents=True, exist_ok=True)

    serverSpaceData = __send_command_to_pkz_servers("df -BG", sshUser)
    serverSpaceData = __filter_server_answer_by_regex(
        serverSpaceData, "(?:\S+\s+){5}/var;|((?:\S+\s+){5}/)(?!.*/var)"
    )

    print("Sorting by used space %")
    serverSpaceData = sorted(
        serverSpaceData.items(), key=lambda item: int(item[1].split()[4][:-1])
    )

    with open(statsFilePath, "w") as statsFile:
        for host,line in serverSpaceData.items():
            statsFile.write(f"{host}; {line};\n")
    print(f"Saved in {statsFilePath}")


def __createServerVersionList(user: str, userHomeDirectory: str, fileName: str):
    statsFileName = f"{fileName}{datetime.datetime.now().strftime('%Y%m%d_%H%M')}"

    fileDirName = "pkzStats"
    statsDirPath = f"{userHomeDir}/{fileDirName}"
    statsFilePath = f"{statsDirPath}/{statsFileName}"
    pathlib.Path(statsDirPath).mkdir(parents=True, exist_ok=True)

    serverVersionData = __send_command_to_pkz_servers("plesk -v", sshUser)
    serverSpaceData = __filter_server_answer_by_regex(serverSpaceData, "Plesk.*")

    print("Sorting by Plesk Version")
    serverVersionData = sorted(
        serverVersionData.items(), key=lambda item: int(item[1])
    )

    with open(statsFilePath, "w") as statsFile:
        for host,line in serverVersionData.items():
            statsFile.write(f"{host}; {line};\n")
    print(f"Saved in {statsFilePath}")


if not any(
    pathlib.Path(f"{userHomeDir}/pkzStats").glob(
        f"{avalSpaceFileName}{datetime.datetime.now().strftime('%Y%m%d')}*"
    )
):
    print("No relevant file with server space was found")
    __createFreeSpaceServerList(sshUser, userHomeDir, avalSpaceFileName)
elif any(
    pathlib.Path(f"{userHomeDir}/pkzStats").glob(
        f"{serverVersionFileName
        }{datetime.datetime.now().strftime('%Y%m%d')}*"
    )
):
    print("No relevant file with server versions was found")
    __createServerVersionList()(sshUser, userHomeDir, avalSpaceFileName)

# spaceDataPath=list(pathlib.Path(f"{userHomeDir}/pkzStats").glob("pleskAvailableSpace*"))[-1]
# versionDataPath=list(pathlib.Path(f"{userHomeDir}/pkzStats").glob("pleskVersion*"))[-1]
# servers = {}
# with open(spaceDataPath) as f:
#     for line in f:
#         line = line.replace("\n", "").replace('G','').split(' ',1)
#         print(line)
#         curServerName=re.search(r"^([^.])+",line[0]).group(0)
#         curServerData=line[1].split(' ')
#         curFilesystem, curTotalSpace, curUsedSpace, curFreeSpace= curServerData[0],int(curServerData[1]),int(curServerData[2]),int(curServerData[3])
#         curServer= pkzServer(curServerName,curFilesystem,curTotalSpace,curUsedSpace,curFreeSpace,'')
#         servers[curServerName]=curServer
# print(servers["pkz44"])
