function vInfoVpsGet  --description "Returns info about given Virtualizor VPS by hostname"    
    set pythonScriptsPath (find ~ -maxdepth 1 -name configBackup  | head -n1)
    set argNum (count $argv)
    if test $argNum -gt 1
        echo Too many arguments [$argnum]
        return 1
    end
    if not set -q argv[1]
        echo Empty input
        return 1
    end
    set vpsHostName (echo $argv)
    set requestResult (curl -s "https://virtualizor.hoster.kz:4085/index.php?act=vs&vpshostname=$vpsHostName&api=json&adminapikey=$VZR_API_KEY&adminapipass=$VZR_API_PASS")
    if not grep -q $vpsHostName (echo $requestResult|psub)
        echo "Host $vpsHostName was not found"
        return 1
    else
        set parsedResult (echo $requestResult | jello -lr '[f"{k}:{v}" for server_record in _.vs.values() for k,v in server_record.iteritems() if k in ["hostname", "vps_name", "vpsid", "os_name", "space", "ram", "cores", "network_speed", "upload_speed", "suspended", "nic_type", "cpu_mode", "server_name", "email", "cached_disk"] or (k == "ips" and {f"ips:{ip}" for ip in v.values()})]')
        set vpsId (string split ":" -f2 $parsedResult[1])
        set vpsVId (string split ":" -f2 $parsedResult[2])
        set vpsHostname (string split ":" -f2 $parsedResult[3])
        set os_name (string split ":" -f2 $parsedResult[4])
        set space (string split ":" -f2 $parsedResult[5])
        set ram (string split ":" -f2 $parsedResult[6])
        set cores (string split ":" -f2 $parsedResult[7])
        set network_speed (string split ":" -f2 $parsedResult[8])
        set upload_speed (string split ":" -f2 $parsedResult[9])
        set suspended (string split ":" -f2 $parsedResult[10])
        set nic_type (string split ":" -f2 $parsedResult[11])
        set cpu_mode (string split ":" -f2 $parsedResult[12])
        set diskInfo (string split ":" -f2 -m1 $parsedResult[13])
        set server_name (string split ":" -f2 $parsedResult[14])
        set email (string split ":" -f2 $parsedResult[15])
        set ip (string split ":" -f2 $parsedResult[16]|grep -Po "((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}")

        
        echo IP\|$ip
        echo ID\\VID\|$vpsId\\$vpsVId
        echo Hostname\|$vpsHostname
        echo User\|$email
        echo Is suspended\|$suspended
        echo Server\|$server_name
        echo OS\|$os_name
        echo NIC\|$nic_type
        echo Space\|$space
        echo RAM\|$ram
        echo CPU mode\|$cpu_mode
        echo Cores\|$cores
        echo Network speed\|$network_speed
        echo Upload speed\|$upload_speed
        return 0 
    end
end
