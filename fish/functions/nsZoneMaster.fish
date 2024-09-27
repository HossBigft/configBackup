function nsZoneMaster --description "Returns zone master value from DNS servers for given domain. Can return only ip with -q/--quiet option"
    set scriptsPath (find ~ -maxdepth 1 -name configBackup  | head -n1)
    python3 $scriptsPath/pyScrs/nsZoneMaster.py  $argv
end
