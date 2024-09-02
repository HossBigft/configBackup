function pCheckSiteBackup --wraps==ssh --wraps=ssh
    set host (echo $argv[1])
    set domain (echo $argv[2])
    ssh $host "find  /backup* -maxdepth 6 -type d -name $domain|xargs du -sh"  
end
