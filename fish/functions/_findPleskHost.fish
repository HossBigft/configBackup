function _findPleskHost
    set domain (echo $argv[1])
    set host (digsx $domain)
    if string match -rq "no Result for" $host
        set host (python3.12 /home/gmv/configBackup/pyScrs/pFindSubscriptionByDomain.py -s $domain)
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
