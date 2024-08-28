function pPhpVersion --wraps=ssh
    set argNum (count $argv)

    if test $argNum -eq 1
        set domain (echo $argv)
        set username (echo $domain|string replace -ar "\.|-" "_")
        set host (_findPleskHost $domain)
        if test $status -eq 1
            echo "Host for $domain was not found"
            return 1
        else
            echo "Host for $domain is $host"
        end
    else if test $argNum -eq 2
        set domain (echo $argv[2])
        set username (echo $domain|string replace -ar "\.|-" "_")
        set host (echo $argv[1])
    end

    ssh maximg@$host "selectorctl --user-summary --user=$username|grep s|cut -d \" \" -f1"
end
