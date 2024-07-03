import shutil
import os.path


backuplist = {"windowsTerminal":("/mnt/c/Users/COMPUTER406_1/AppData/Local/Packages/Microsoft.WindowsTerminal_8wekyb3d8bbwe/LocalState/settings.json",os.path.dirname(__file__)+"/")
,"gitConfig":("/mnt/c/Users/COMPUTER406_1/.gitconfig",os.path.dirname(__file__)+"/")
,"espansoConfig":("/mnt/c/Users/COMPUTER406_1/AppData/Roaming/espanso/match/base.yml",os.path.dirname(__file__)+"/")
,"fluentSearch":("/mnt/c/Users/COMPUTER406_1/Documents/GluschenkoMV/progs/fluent_search_backup",os.path.dirname(__file__)+"/fluentSearchBackup")

              
}
for configName, srcDst in backuplist.items():
    print(f"Copying {configName} from {srcDst[0]}")
    src =srcDst [0]
    dst =srcDst [1]
    if os.path.isfile(src):
        shutil.copy2(src,dst)
    else:
        shutil.copytree(src, dst, dirs_exist_ok=True)
