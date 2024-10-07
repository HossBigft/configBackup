function pPhpDebugToggle --wraps=ssh
    set -l options l/literal
    argparse -n pPhpDebugToggle $options -- $argv
    or return
    
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
        
        if set -q _flag_literal
            set username (echo $domain)
        else    
            set username (_pDomainToCageFsUsername $host $subscriptionName)
        end
    end
        ssh $host "curPHPVersion=\$(selectorctl --user-summary --user=$username|grep s|cut -d \" \" -f1); displayErrorsValue=\$(selectorctl  --print-options --version=\$curPHPVersion --user=$username --csv|grep -Po \"display_errors.*\"on\"\"); if [[ \$displayErrorsValue ]]; then selectorctl --replace-options=display_errors:off --version=\$curPHPVersion --user=$username && echo \"display_errors:off for user $username PHP \$curPHPVersion\"; else selectorctl --replace-options=display_errors:on --version=\$curPHPVersion --user=$username && echo \"display_errors:on for user $username PHP \$curPHPVersion\"; fi"
        return 0
end
