import subprocess,re,pathlib, shlex
from dataclasses import dataclass
@dataclass
class pkzServer:
    name: str
    mainFileSystem: str
    totalSpace: int
    usedSpace: int
    freeSpace: int
    pleskVersion: str
hosts=("185.111.106.116","185.129.51.20")

userHomeDir=pathlib.Path.home()
pathlib.Path(f"{userHomeDir}/pkzStats").mkdir(parents=True, exist_ok=True)
for host in hosts:
    cmd = shlex.split(f"ssh root@{host} df -BG")
    print(cmd)
    sshOutput = subprocess.run(cmd,capture_output=True, text=True)
    print(sshOutput.stdout)
# result = subprocess.run(["df", "-BG"],capture_output=True, text=True)
# result = result.stdout.splitlines()
# result = [" ".join(line.split()) for line in result]
# result = "".join(filter(lambda s: re.fullmatch("(?:\S+\s+){5}/var;|((?:\S+\s+){5}/)(?!.*/var)",s),result))

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



