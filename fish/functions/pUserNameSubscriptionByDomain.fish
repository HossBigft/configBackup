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

    ssh $host "plesk db -Ne \"SELECT DISTINCT c.login AS 'Customer Username' FROM data_bases db JOIN domains d ON db.dom_id = d.id JOIN clients c ON d.cl_id = c.id WHERE d.id = (SELECT CASE WHEN webspace_id = 0 THEN id ELSE webspace_id END AS result FROM domains WHERE name LIKE '$domain%');\""
end
