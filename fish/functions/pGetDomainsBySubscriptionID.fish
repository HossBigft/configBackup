function pGetDomainsBySubscriptionID --wraps=ssh
    set host (echo $argv[1])
    set subscriptionID (echo $argv[2])

    ssh $host "plesk db -Ne \"SELECT name FROM domains WHERE webspace_id=$subscriptionID OR (webspace_id=0 AND id=$subscriptionID)\""

end
