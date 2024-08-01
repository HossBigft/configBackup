function nsGetSubDomains
    set -l options v/verbose
    argparse -n nsGetSubDomains $options -- $argv
    or return
    set domain (echo $argv|string lower)
    set dnsServers (cat ~/.ssh/config|grep -Po "(?<=Hostname ).*|(?<=HostName ).*"|grep -Po "ns.*")
    
    if set -q _flag_verbose
        echo Querying Hoster.KZ DNS servers about $argv
        for host in $dnsServers
            echo (echo $host|grep -Po "^([^.])+")\|
            ssh root@$host "cat /var/opt/isc/scls/isc-bind/zones/_default.nzf" | grep $domain | grep -Po "(?<=\").*?(?=\" )"
        end
        return 0
    end
    
    ssh root@$dnsServers[1] "cat /var/opt/isc/scls/isc-bind/zones/_default.nzf" | grep $domain | grep -Po "(?<=\").*?(?=\" )"
end
