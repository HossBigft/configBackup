function nsZoneMaster
    set dnsServers (cat ~/.ssh/config|grep -Po "(?<=Hostname ).*|(?<=HostName ).*"|grep -Po "ns.*")
    set domains (echo $argv | string split " ")
    set domainCount (count $domains)
    
    if test $domainCount -eq 1
        echo Querying Hoster.KZ DNS servers about $argv
        for host in $dnsServers
            set zoneMaster (ssh root@$host "cat /var/opt/isc/scls/isc-bind/zones/_default.nzf"| grep \"$argv\" | grep -Po "((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}")
            echo (echo $host|grep -Po "^([^.])+")\|  $zoneMaster\|

            if set digAnswer (fish -c "digsx $zoneMaster")
                echo $digAnswer
            end
        end
    else
        for domain in $domains
            echo Querying Hoster.KZ DNS servers about $domain
            for host in $dnsServers
                set zoneMaster (ssh root@$host "cat /var/opt/isc/scls/isc-bind/zones/_default.nzf"| grep \"$domain\" | grep -Po "((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}")
                echo (echo $host|grep -Po "^([^.])+")\|  $zoneMaster\|

                if set digAnswer (fish -c "digsx $zoneMaster")
                    echo $digAnswer
                end
            end
        end
    end
end
