function pPhpSetVersion --wraps=ssh
    set argNum (count $argv)
    set availablePhpRegex "4.4|5.1|5.2|5.3|5.4|5.5|5.6|7.0|7.1|7.2|7.3|7.4|8.0|8.1|8.2|8.3"
    if test $argNum -eq 2
        set domain (echo $argv[1])
        set phpVersion (echo $argv[2])
        if contains $phpVersion (string split "|" $availablePhpRegex)
            set host (_findPleskHost $domain)
            if test $status -eq 0
                echo (color_word blue "[FOUND]")" Host for $domain is "(color_word yellow $host)
            else
                echo (color_word red "[ERROR]")" Host for $domain was not found."
                return 1
            end
            
            set subscriptionName (pSubscriptionNameByDomain $host $domain -q)
            if test $status -ne 0
                echo (color_word red "[ERROR]")" Subscription $subscriptionName was not found on $host"
                return 1
            else
                echo (color_word blue "[FOUND]")" subscription $subscriptionName on $host."
            end
            
            set username (_pDomainToCageFsUsername $host $subscriptionName)
            if test $status -ne 0
                echo (color_word red "[ERROR]")" CageFS user for subscription $subscriptionName was not found."
                return 1
            else
                echo (color_word blue "[FOUND]")" CageFS user $username for subscription $subscriptionName"
            end
            
            
            ssh $host "selectorctl --set-user-current=$phpVersion --user=$username"
            if test $status -eq 0
                printf (echo (color_word green "[SET]"))" PHP %s for subscription %s with user %s.\n" $phpVersion $subscriptionName $username
            end
            return $status
        else
            echo (color_word red "[ERROR]")" PHP $phpVersion not available."
            echo "Available PHP versions: $availablePhpRegex"
            return 1
        end
    else if test $argNum -eq 3
        set host (echo $argv[1])
        
        if not _isExistingPleskHost $host
           echo (color_word red "[ERROR]")" Host $host does not exist."
            return 1
        end
        
        set phpVersion (echo $argv[3])
        
        if string match -aqr $phpVersion $availablePhpRegex
            set subscriptionName (echo $argv[2])
            set username (_pDomainToCageFsUsername $host $subscriptionName)
            if test $status -ne 0
                set_color red; echo "[ERROR] CageFS user for subscription $subscriptionName was not found."
                return 1
            else
                echo (color_word blue "[FOUND]")" CageFS user $username for subscription $subscriptionName"
            end
            
            ssh $host "selectorctl --set-user-current=$phpVersion --user=$username"
            
            if test $status -eq 0
               printf (echo (color_word green "[SET]"))" PHP %s for subscription %s with user %s.\n" $phpVersion $subscriptionName $username
            end
        else
            echo (color_word red "[ERROR]")" PHP $phpVersion not available."
            echo "Available PHP versions: $availablePhpRegex"
            return 1
        end
    else
        echo (color_word red "[ERROR]")" wrong number of arguments[$argNum]"
    end

end
