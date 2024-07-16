function nsRmZoneMaster
set dnsServers (cat ~/.ssh/config|grep -Po "(?<=Hostname ).*|(?<=HostName ).*"|grep -Po "ns.*")
    for host in $dnsServers
        echo $host "/opt/isc/isc-bind/root/usr/sbin/rndc delzone -clean $argv"
        ssh root@$host "/opt/isc/isc-bind/root/usr/sbin/rndc delzone -clean $argv"
    end
end
