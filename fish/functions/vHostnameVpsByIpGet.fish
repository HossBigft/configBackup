function vHostnameVpsByIpGet
    set argNum (count $argv)
    if test $argNum -gt 1
        echo Too many arguments [$argnum]
        return 1
    end
    if not set -q argv[1]
        echo Empty input
        return 1
    end
    set vpsIp (echo $argv)
    set requestResult (curl -s "https://virtualizor.hoster.kz:4085/index.php?act=vs&api=json&adminapikey=$VZR_API_KEY&adminapipass=$VZR_API_PASS&vpsip=$vpsIp")
    if not grep -q $vpsIp (echo $requestResult|psub)
        echo "Host with IP $vpsIp was not found"
        return 1
    else
        echo $requestResult | jello  -rl jello '[server_record.hostname for server_record in _.vs.values() ]'
        return 0
    end
end
