function pMailCredentialsTestGet
    set argNum (count $argv)

    if test $argNum -eq 1
        set domain (echo $argv)
        set host (_findPleskHost $domain)
        if test -z "$host"
            echo "Host for $domain was not found"
            return 1
        else
            echo "Host for $domain is $host"
        end
    else if test $argNum -eq 2
        set domain (echo $argv[2])
        set host (echo $argv[1])
    else
        echo Wrong input
        return 1
    end
    set testMail testhostermail
    echo "Login link:https://webmail.$domain/roundcube/index.php?_user=$testMail%40$domain"
    echo password: (ssh $host  "plesk bin mail --info testhostermail@$domain" | grep Description | string replace -r ' +' ' ' | string split " " -f2)
    return 0
end
