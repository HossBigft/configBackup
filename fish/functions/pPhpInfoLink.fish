function pPhpInfoLink --description 'generates link to open phpinfo() for given domain in admin panel'
    set argNum (count $argv)

    if test $argNum -eq 1 
        set domain (echo $argv)
        set host (_findPleskHost $domain)
        if test -z "$host"
            echo "Host for $domain was not found"
            return 1
        else
            echo "Host for $domain is $host"
        end
    else if test $argNum -eq 2 
        set domain (echo $argv[2])
        set host (echo $argv[1])
    else
        echo Wrong input
        return 1
    end
    set subscriptionId (pSubscriptionIDByDomain $host $domain)
    if test $status -eq 1
        echo No subscription with domain $domain  on $host
        return 1
    end

    set redirectionHeader "&success_redirect_url=%2Fsmb%2Fweb%2Fphp-info%2Fid%2F$subscriptionId"
    set phpInfoLink (plog $host)
    if test $status -eq 1
        echo "Php info link generation for $host failed"
        return 1
    end

    echo $phpInfoLink$redirectionHeader
    return 0
end
