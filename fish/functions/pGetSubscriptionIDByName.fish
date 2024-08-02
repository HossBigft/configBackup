function pGetSubscriptionIDByName --wraps=ssh
    set host (echo $argv[1])
    set domain (echo $argv[2])

    ssh $host "plesk db -Ne \"SELECT id FROM domains WHERE name LIKE '%$domain%'\""|grep -Pv "^0\$"| sort -u
end
