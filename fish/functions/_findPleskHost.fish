function _findPleskHost --description "Tries to find Plesk server hostname by given domain"
    set scriptsPath (find ~ -maxdepth 1 -name configBackup  | head -n1)
    python3 $scriptsPath/pyScrs/pFindPleskHostByDomain.py $argv
end
