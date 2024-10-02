function vInfoVpsGet  --description "Returns info about given Virtualizor VPS by hostname"
    set scriptsPath (find ~ -maxdepth 1 -name configBackup  | head -n1)

    python3  $scriptsPath/pyScrs/printVpsInfoVirtualizor.py $argv
end
