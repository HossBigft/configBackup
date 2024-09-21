function geoIpQuery --description 'Return geo data about IP. Uses ipinfo.io'
    set ipList (echo $argv | string split " " -n)
    for ip in $ipList
        if not string match -qr "((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}" $ip
            echo 'Input should be IP or list of IPs'
            return 1
        end
    end 
    for ip in $ipList
        set parsedRequest (curl -s https://ipinfo.io/$ip|jello -lr '[f"{k}:{v}" for k,v in _.iteritems() if k  in ["ip", "country", "org"]]'&& echo PTR:(digsx $ip) )
        string repeat "⋁" -n (string split "" $parsedRequest[1]|count)
        printf %s\n $parsedRequest
        string repeat "⋀" -n (string split "" $parsedRequest[4]|count)
    end
    return 0
end
