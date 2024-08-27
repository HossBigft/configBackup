function pMailGetList --wraps=ssh
    set argNum (count $argv)
    
    if test $argNum -eq 1
        set domain (echo $argv)
        set host (_findPleskHost $domain)
        if test -z "$host"
            echo "Host for $domain was not found"
            return 1
        else
            echo "Host for $domain is $host"
        end
    else if test $argNum -eq 2
        set domain (echo $argv[2])
        set host (echo $argv[1])
    end
    ssh maximg@$host "plesk bin mail --list"|grep $domain
end
