function pRestartDnsServiceForDomains --wraps==ssh --wraps=ssh
    set host (echo $argv[1])
    set domains (echo $argv[2]|string split " " -n)
    echo $domains
    for domain in $domains
        echo "restarting DNS service for $domain"
        ssh $host "plesk bin dns --off $domain && plesk bin dns --on $domain"
    end
end
