import shutil
import os.path


backuplist = {"windowsTerminal":("/mnt/c/Users/COMPUTER406_1/AppData/Local/Packages/Microsoft.WindowsTerminal_8wekyb3d8bbwe/LocalState/settings.json",os.path.dirname(__file__)+"/")
,"gitConfig":("/mnt/c/Users/COMPUTER406_1/.gitconfig",os.path.dirname(__file__)+"/")
}
for configName, srcDst in backuplist.items():
    print(f"Copying {configName} from {srcDst[0]}")
    src =srcDst [0]
    dst =srcDst [1]
    shutil.copy2(src,dst)
