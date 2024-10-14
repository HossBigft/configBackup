function nsRmZoneMaster --description "Removes zone for given domain from DNS slave servers"

    set domains (echo $argv)
    nsZoneMaster $argv
    set dnsServers (cat ~/.ssh/config|grep -Po "(?<=Hostname ).*|(?<=HostName ).*"|grep -Po "ns.*")
    for domain in $domains
        for host in $dnsServers
            echo $host "/opt/isc/isc-bind/root/usr/sbin/rndc delzone -clean $domain"
            ssh $host "/opt/isc/isc-bind/root/usr/sbin/rndc delzone -clean $domain"
        end
    end
    nsZoneMaster $argv
end
