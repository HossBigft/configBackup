function pPhpDebugToggle --wraps=ssh
    set argNum (count $argv)

    if test $argNum -eq 1
        set domain (echo $argv)
        set username (echo $domain|string replace -ar "\.|-" "_")
        set host (digsx $domain)
        if string match -qr "no Result for" $host
            echo $host
            return 1
        else 
            echo Server $host
        end
    else if test $argNum -eq 2
        set domain (echo $argv[2])
        set username (echo $domain|string replace -ar "\.|-" "_")
        set host (echo $argv[1])
    end
        ssh maximg@$host "curPHPVersion=\$(selectorctl --user-summary --user=$username|grep s|cut -d \" \" -f1); displayErrorsValue=\$(selectorctl  --print-options --version=\$curPHPVersion --user=$username --csv|grep -Po \"display_errors.*\"on\"\"); if [[ \$displayErrorsValue ]]; then selectorctl --replace-options=display_errors:off --version=\$curPHPVersion --user=$username && echo \"display_errors:off for user $username PHP \$curPHPVersion\"; else selectorctl --replace-options=display_errors:on --version=\$curPHPVersion --user=$username && echo \"display_errors:on for user $username PHP \$curPHPVersion\"; fi"
        return 0
end
