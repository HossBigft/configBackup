function pMailBlacklistDomain --wraps=ssh
    set host (echo $argv[1])
    set domain (echo $argv[2])

    ssh $host "plesk bin mailserver --add-to-black-list $domain"
    printf "Domain %s was added to mail server spamlist on %s" $domain $host
    ssh $host "plesk bin mailserver --info black-list" 
end
