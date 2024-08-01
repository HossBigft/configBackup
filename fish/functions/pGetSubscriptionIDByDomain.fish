function pGetSubscriptionIDByDomain --wraps=ssh
    set host (echo $argv[1])
    set domain (echo $argv[2])

    ssh $host "plesk db -Ne \"SELECT webspace_id FROM domains WHERE name LIKE '%$domain%'\""|grep -v 0| sort -u
    
end
