function _findPleskHost --description "Tries to find Plesk server hostname by given domain"
    set scriptsPath (find ~ -name configBackup | head -n1)
    python3 $scriptsPath/pyScrs/findPleskHostByDomain.py $argv
end
