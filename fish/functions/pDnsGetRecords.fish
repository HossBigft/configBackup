function pDnsGetRecords
    set argNum (count $argv)
    
    if test $argNum -eq 1
        set domain (echo $argv)
        set host (_findPleskHost $domain)
        if test $status -eq 1
            echo "Host for $domain was not found"
            return 1
        else
            echo "Host for $domain is $host"
        end
    else if test $argNum -eq 2
        set domain (echo $argv[2])
        set host (echo $argv[1])
    else
        echo Wrong input
        return 1
    end
    
    ssh $host "plesk bin dns --info $domain" | awk NF | head -n -1 | sort -k2; 
    return 0
end
