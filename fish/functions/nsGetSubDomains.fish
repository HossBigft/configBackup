function nsGetSubDomains
    set -l options q/quiet
    argparse -n nsGetSubDomains $options -- $argv
    or return
    set dnsServers (cat ~/.ssh/config|grep -Po "(?<=Hostname ).*|(?<=HostName ).*"|grep -Po "ns.*")
    if set -q _flag_quiet
        ssh root@$dnsServers[1] "cat /var/opt/isc/scls/isc-bind/zones/_default.nzf" | grep $argv | grep -Po "(?<=\").*?(?=\" )"
        return 0
    end
    echo Querying Hoster.KZ DNS servers about $argv
    for host in $dnsServers
        echo (echo $host|grep -Po "^([^.])+")\|
        ssh root@$host "cat /var/opt/isc/scls/isc-bind/zones/_default.nzf" | grep $argv | grep -Po "(?<=\").*?(?=\" )"
    end
end
