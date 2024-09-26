function pUserNameSubscriptionByDomain --wraps=ssh --description 'Returns username of subscription that holds given domain. Can search hosts'
    set -l options q/quiet
    argparse -n pUserNameSubscriptionByDomain $options -- $argv
    or return

    set argNum (count $argv)

    if test $argNum -eq 1 
        set domain (echo $argv)
        set host (_findPleskHost $domain)
        if not set -q _flag_quiet
            if test -z "$host"
                echo "Host for $domain was not found"
                return 1
            else
                echo "Host for $domain is $host"
            end
        end
    else if test $argNum -eq 2 
        set domain (echo $argv[2])
        set host (echo $argv[1])
    else
        echo Wrong input
        return 1
    end

    ssh $host "plesk db -Ne \"SELECT login FROM clients WHERE id=(SELECT cl_id FROM domains WHERE name LIKE '$domain%');\""
end
