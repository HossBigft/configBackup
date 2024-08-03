function pGetSubscriptionIDByDomain --wraps=ssh
    set argNum (count $argv)
    
    if test $argNum -eq 1
        set domain (echo $argv)
        set host (digs $domain|string sub -e-1)

        ssh $host "plesk db -Ne \"SELECT webspace_id FROM domains WHERE name LIKE '%$domain%'\""|grep -Pv "^0\$"| sort -u
        
    else if test $argNum -eq 2
        set host (echo $argv[1])
        set domain (echo $argv[2])

        ssh $host "plesk db -Ne \"SELECT webspace_id FROM domains WHERE name LIKE '%$domain%'\""|grep -Pv "^0\$"| sort -u
    end
end
