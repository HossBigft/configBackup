function pPhpExtensionsGet --wraps=ssh
    set argNum (count $argv)
    set availablePhpRegex "4.4|5.1|5.2|5.3|5.4|5.5|5.6|7.0|7.1|7.2|7.3|7.4|8.0|8.1|8.2|8.3"
    
    if test $argNum -eq 1
        set domain (echo $argv)
        set host (digsx $argv)
        set host (_findPleskHost $domain)
        if test -z "$host"
            echo "Host for $domain was not found"
            return 1
        else
            echo "Host for $domain is $host"
        end
        
        set username (echo $domain|string replace "." "_")
        ssh maximg@$host "curPHPVersion=\$(selectorctl --user-summary --user=$username|grep s|cut -d \" \" -f1)&& selectorctl --list-user-extensions --version=\$curPHPVersion --user=$username"
        return 0
        
    else if test $argNum -eq 2
        set host (echo $argv[1])
        set domain (echo $argv[2])
        set username (echo $domain|string replace "." "_")
        ssh maximg@$host "curPHPVersion=\$(selectorctl --user-summary --user=$username|grep s|cut -d \" \" -f1)&& selectorctl --list-user-extensions --version=\$curPHPVersion --user=$username"
        return 0
        
    else if test $argNum -eq 3
        set phpVersion (echo $argv[3])
        if string match -aqr $phpVersion $availablePhpRegex
            set host (echo $argv[1])
            set domain (echo $argv[2])
            set username (echo $domain|string replace "." "_")
            ssh maximg@$host "selectorctl --list-user-extensions --version=$phpVersion --user=$username"
            return 0
        else
            printf "Available PHP versions: $availablePhpRegex\n"
            return 1
        end
    end
end
