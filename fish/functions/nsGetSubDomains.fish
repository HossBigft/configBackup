function nsGetSubDomains
    set dnsServers (cat ~/.ssh/config|grep -Po "(?<=Hostname ).*|(?<=HostName ).*"|grep -Po "ns.*")
    echo Querying Hoster.KZ DNS servers about $argv
    for host in $dnsServers
        echo (echo $host|grep -Po "^([^.])+")\|
        ssh root@$host "cat /var/opt/isc/scls/isc-bind/zones/_default.nzf" | grep $argv | grep -Po "(?<=\").*?(?=\" )"
    end
end
