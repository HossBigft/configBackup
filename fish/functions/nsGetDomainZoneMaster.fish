function nsGetDomainZoneMaster
    set dnsServers (cat ~/.ssh/config|grep -Po "(?<=Hostname ).*|(?<=HostName ).*"|grep -Po "ns.*")
    echo Querying Hoster.KZ DNS servers about $argv
    for host in $dnsServers
        set zoneMaster (ssh root@$host "cat /var/opt/isc/scls/isc-bind/zones/_default.nzf"| grep \"$argv\" | grep -Po "((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}")
        echo (echo $host|grep -Po "^([^.])+")  $zoneMaster
    end
end
