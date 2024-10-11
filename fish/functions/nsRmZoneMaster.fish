function nsRmZoneMaster --description "Removes zone for given domain from DNS slave servers"

    set domain (echo $argv)
    nsZoneMaster  $domain
    set dnsServers (cat ~/.ssh/config|grep -Po "(?<=Hostname ).*|(?<=HostName ).*"|grep -Po "ns.*")
    for host in $dnsServers
        echo $host "/opt/isc/isc-bind/root/usr/sbin/rndc delzone -clean $domain"
        ssh $host "/opt/isc/isc-bind/root/usr/sbin/rndc delzone -clean $domain"
    end
    nsZoneMaster  $domain
end
