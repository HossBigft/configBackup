function pPhpOptionsGet --wraps=ssh  --description "Returns list of custom PHP options set in PHP selector, such as debug"

    set argNum (count $argv)

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
    else if test $argNum -eq 2
        set subscriptionName (echo $argv[2])
        set host (echo $argv[1])
        set username (_pDomainToCageFsUsername $host $subscriptionName)
    end
    
    ssh $host "curPHPVersion=\$(selectorctl --user-summary --user=$username|grep s|cut -d \" \" -f1);selectorctl  --print-options --version=\$curPHPVersion --user=$username --json" | jello -s|grep "\.value"| string replace "_.data." ""

end
