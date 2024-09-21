function pMailTestCreate --wraps=ssh --description "Creates test mail account for given domain. If it's already created, returns logpass. Can also remove test account with -r/--remove flag"
    set -l options r/remove
    argparse -n pMailTestCreate $options -- $argv
    or return

    set argNum (count $argv)
    set testMail testhostermail

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
    if set -q _flag_remove
        ssh host "plesk bin mail --remove $testMail@$domain"
        if test $status eq 0
            echo Email $testMail@$domain is removed
            return 0
        else
            return 1
        end
    end


    set password (ssh $host  "plesk bin mail --info $testMail@$domain" | grep Description | string replace -r ' +' ' ' | string split " " -f2)
    if test -n "$password"
        set password (pwgen 20 | string split " " -f1)
        ssh $host "plesk bin mail --create $testMail@$domain -passwd \"$password\" -mailbox true -description \"$password\""
        if test $status -eq 0
            echo "Login link:https://webmail.$domain/roundcube/index.php?_user=$testMail%40$domain"
            echo $password
            return 0
        else
            return 1
        end
    else
        echo "Login link:https://webmail.$domain/roundcube/index.php?_user=$testMail%40$domain"
        echo $password
        return 0
    end

end
