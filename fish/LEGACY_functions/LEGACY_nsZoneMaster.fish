function nsZoneMaster --description "Returns zone master value from DNS servers for given domain. Can return only ip with -q/--quiet option"
    set -l options q/quiet
    argparse -n nsZoneMaster $options -- $argv
    or return

    set dnsServers (cat ~/.ssh/config|grep -Po "(?<=Hostname ).*|(?<=HostName ).*"|grep -Po "ns.*")
    set domains (echo $argv | string split " ")
    set domainCount (count $domains)

    if test $domainCount -eq 1
        if not set -q _flag_quiet
            echo Querying Hoster.KZ DNS servers about $argv
        end
        for host in $dnsServers
            set zoneMaster (ssh $host "cat /var/opt/isc/scls/isc-bind/zones/_default.nzf"| grep \"$argv\" | grep -Po "((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}")

            if set -q _flag_quiet
                echo $zoneMaster
            else
                echo (echo $host|grep -Po "^([^.])+")\| $zoneMaster\|

                if set digAnswer (digsx $zoneMaster)
                    echo $digAnswer
                end
            end
        end
    else
        for domain in $domains
            echo Querying Hoster.KZ DNS servers about $domain
            for host in $dnsServers
                set zoneMaster (ssh $host "cat /var/opt/isc/scls/isc-bind/zones/_default.nzf"| grep \"$domain\" | grep -Po "((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}")

                if set -q _flag_quiet
                    echo $zoneMaster
                else
                    echo (echo $host|grep -Po "^([^.])+")\| $zoneMaster\|

                    if set digAnswer (digsx $zoneMaster)
                        echo $digAnswer
                    end
                end
            end
        end
    end
end
