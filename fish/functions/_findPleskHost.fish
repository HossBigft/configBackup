function _findPleskHost
    set domain (echo $argv[1])
    set host (digsx $domain)
    if string match -rq "no Result for" $host; or not string match -rq "hoster.kz"
        set host (python3.12 /home/gmv/configBackup/pyScrs/pFindSubscriptionByDomain.py -s $domain|string collect)
        
        if test (echo $host | string split "\n" | count) -gt 1
            echo Multiple hosts found 
            echo $host
            return 1
        end
        
        if string match -rq "No servers was found" $host 
            return 1
        else
            echo $host
            return 0
        end
    else
        echo $host
        return 0
    end
end
