function pGetSubscriptionNameByDomain --wraps=ssh
    set host (echo $argv[1])
    set domain (echo $argv[2])
    set subscriptionID (pGetSubscriptionIDByDomain $host $domain)
    pGetSubscriptionNameByID $host $subscriptionID

end
