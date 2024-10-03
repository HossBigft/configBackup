function pPhpVersion --wraps=ssh --description 'Returns current PHP version set in PHP Selector. Takes either hostname and subscription name or tries to find host by subscription name'
    set -l options l/literal
    argparse -n pPhpVersion $options -- $argv
    or return
    
    set argNum (count $argv)

    if test $argNum -eq 1
        set domain (echo $argv)
        set subscriptionName (pSubscriptionNameByDomain $domain -q)
        set host (_findPleskHost $domain)
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
        
        if set -q _flag_literal
            set username (echo $domain)
        else    
            set username (_pDomainToCageFsUsername $host $subscriptionName)
        end
        
    end

    ssh maximg@$host "selectorctl --user-summary --user=$username|grep s|cut -d \" \" -f1"
end
