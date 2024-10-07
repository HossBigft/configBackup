function pPhpExtensionsGet --wraps=ssh
    set argNum (count $argv)
    set availablePhpRegex "4.4|5.1|5.2|5.3|5.4|5.5|5.6|7.0|7.1|7.2|7.3|7.4|8.0|8.1|8.2|8.3"
    
    if test $argNum -eq 1
        set domain (echo $argv)
        set host (_findPleskHost $domain)
        set subscriptionName (pSubscriptionNameByDomain $host $domain -q)
        set username (_pDomainToCageFsUsername $host $subscriptionName)
        
        if test $status -ne 0
            echo "[ERROR] CageFS user for subscription $subscriptionName was not found."
        else
            echo "Found CageFS user $username for subscription $subscriptionName."
        end
        
        if test $status -eq 1
            echo "[ERROR] Host for $domain was not found"
            return 1
        else
            echo "Host for $domain is $host"
        end
        ssh $host "curPHPVersion=\$(selectorctl --user-summary --user=$username|grep s|cut -d \" \" -f1)&& selectorctl --list-user-extensions --version=\$curPHPVersion --user=$username"
        return 0
    else if test $argNum -eq 2
        set host (echo $argv[1])
        set domain (echo $argv[2])
        set username (_pDomainToCageFsUsername $host $domain)
        ssh $host "curPHPVersion=\$(selectorctl --user-summary --user=$username|grep s|cut -d \" \" -f1)&& selectorctl --list-user-extensions --version=\$curPHPVersion --user=$username"
        return 0
        
    else if test $argNum -eq 3
        set phpVersion (echo $argv[3])
        if string match -aqr $phpVersion $availablePhpRegex
            set host (echo $argv[1])
            set domain (echo $argv[2])
            set username (_pDomainToCageFsUsername $host $domain)
            ssh $host "selectorctl --list-user-extensions --version=$phpVersion --user=$username"
            return 0
        else
            printf "Available PHP versions: $availablePhpRegex\n"
            return 1
        end
    end
end
