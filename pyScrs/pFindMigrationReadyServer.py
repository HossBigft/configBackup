import subprocess,re,pathlib, shlex, datetime
from dataclasses import dataclass
from collections import namedtuple

@dataclass
class pkzServer:
    name: str
    mainFileSystem: str
    totalSpace: int
    usedSpace: int
    freeSpace: int
    pleskVersion: str

hosts=(
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

sshUser="maximg"

statsFileName=f"TESTpleskAvalSpaceList{datetime.datetime.now().strftime('%Y%m%d_%H%M')}"
fileDirName="pkzStats"
userHomeDir=pathlib.Path.home()
statsDirPath=f"{userHomeDir}/{fileDirName}"
statsFilePath=f"{statsDirPath}/{statsFileName}"
pathlib.Path(statsDirPath).mkdir(parents=True, exist_ok=True)

serverSpaceData=[]
dataRecord = namedtuple('dataRecord', ['host', 'data'])
for host in hosts:
    cmd = f"ssh {sshUser}@{host} df -BG"
    print(f"Querying {host}")
    sshOutput = subprocess.run(shlex.split(cmd),capture_output=True, text=True)
    result=sshOutput.stdout.splitlines()
    result = [" ".join(line.split()) for line in result]
    result = "".join(filter(lambda s: re.fullmatch("(?:\S+\s+){5}/var;|((?:\S+\s+){5}/)(?!.*/var)",s),result))
    print(f"{host} answered {result}")
    serverSpaceData.append(dataRecord(host,result))
print(serverSpaceData)
with open(statsFilePath, 'w') as statsFile:  
    for line in serverSpaceData:    
         statsFile.write(f"{line.host}; {line.data};\n")
print(f"Saved in {statsFilePath}")

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



