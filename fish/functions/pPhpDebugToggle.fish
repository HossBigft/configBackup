function pPhpDebugToggle --wraps=ssh
    set -l options n/name
    argparse -n pPhpDebugToggle $options -- $argv
    or return
    
    set argNum (count $argv)
    if test $argNum -eq 1
        set domain (echo $argv)
        if set -q _flag_name
            set username (echo $domain)
        else
            set username (_pDomainToCageFsUsername $domain)
        end
        set host (_findPleskHost (_pDomainToCageFsUsername -r $domain))
        if test -z "$host"
            echo "Host for $domain was not found"
            return 1
        else
            echo "Host for $domain is $host"
        end
    else if test $argNum -eq 2
        set host (echo $argv[1])
        set domain (echo $argv[2])
        if set -q _flag_name
            set username (echo $domain)
        else
            set username (_pDomainToCageFsUsername $domain)
        end
    end
        ssh maximg@$host "curPHPVersion=\$(selectorctl --user-summary --user=$username|grep s|cut -d \" \" -f1); displayErrorsValue=\$(selectorctl  --print-options --version=\$curPHPVersion --user=$username --csv|grep -Po \"display_errors.*\"on\"\"); if [[ \$displayErrorsValue ]]; then selectorctl --replace-options=display_errors:off --version=\$curPHPVersion --user=$username && echo \"display_errors:off for user $username PHP \$curPHPVersion\"; else selectorctl --replace-options=display_errors:on --version=\$curPHPVersion --user=$username && echo \"display_errors:on for user $username PHP \$curPHPVersion\"; fi"
        return 0
end
