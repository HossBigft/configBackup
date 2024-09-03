function pCheckSiteBackup --wraps==ssh --wraps=ssh
    set host (echo $argv[1])
    set domain (echo $argv[2])
    ssh $host "find  /backup* -maxdepth 6 -type d -name $domain* | sort | tail -n1 | xargs du -am --max-depth=1 | awk '{printf \"%.3f MiB %s\n\", \$1/1024, \$2}'"  
end
