function pCheckSiteBackup --wraps==ssh --wraps=ssh
    set host (echo $argv[1])
    set domain (echo $argv[2])
    ssh $host "find  /backup*/*/clients/ -maxdepth 6 -type d -name $domain* | sort | tail -n1 | xargs du -ak --max-depth=1 | sort -h | awk '{printf \"%.3f MiB %s\n\", \$1/1024, \$2}'"  
end
