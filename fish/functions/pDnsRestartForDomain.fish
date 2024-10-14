function pDnsRestartForDomain  --wraps=ssh --description "Restarts DNS service in Plesk for given domain. Takes server hostname and list of domains. Example pDnsRestartForDomain p-cloud-4 gruzo.kz"
    set host (echo $argv[1])
    set domains (echo $argv[2]|string split " " -n)
    for domain in $domains
        echo "restarting DNS service for $domain"
        ssh $host "plesk bin dns --off $domain && plesk bin dns --on $domain"
    end
end
