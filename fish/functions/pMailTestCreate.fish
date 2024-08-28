function pMailTestCreate --wraps=ssh
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

    set testMail "testhostermail"
    set password (pwgen | string split " " -f1)
    ssh maximg@$host "plesk bin mail --create $testMail@$domain -passwd \"$password\" -mailbox true -description \"$password\""
    echo "Login link:https://webmail.$domain/roundcube/index.php?_user=$testMail%40$domain"
    echo $password
    return 1
end
