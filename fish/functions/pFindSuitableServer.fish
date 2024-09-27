function pFindSuitableServer
    set scriptsPath (find ~ -maxdepth 1 -name configBackup  | head -n1)
    python3  $scriptsPath/pyScrs/pFindMigrationReadyServer.py $argv
    return $status
end
