function vGetVpsIpByHostname
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
        echo $requestResult | jello  -rl '[ip for server_record in _.vs.values() for ip in server_record.ips.values()]'
        return 0 
    end
end
