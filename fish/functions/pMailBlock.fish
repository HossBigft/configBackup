function pMailBlock --wraps=ssh --description 'Changes password of given email and sets outgoing email limit to 0. Can search hosts'
    set argNum (count $argv)
    
        if test $argNum -eq 1 
            set domain (echo $argv | grep -Po "([^@])+\$")
            set host (_findPleskHost $domain)
            set email (echo $argv)
            if not set -q _flag_quiet
                if test -z "$host"
                    echo "Host for $domain was not found"
                    return 1
                else
                    echo "Host for $domain is $host"
                end
            end
        else if test $argNum -eq 2 
            set email (echo $argv[2])
            set domain (echo $argv[2] | grep -Po "([^@])+\$")
            set host (echo $argv[1])
        else
            echo Wrong input
            return 1
        end
        set password (pwgen 20 | string split " " -f1)
        ssh $host "echo Current password is \$(/usr/local/psa/admin/bin/mail_auth_view | grep $email | tr -s ' ' | awk '{print \$5}') && plesk bin mail -u $email -passwd '$password' 1> /dev/null && echo Password for $email is updated && plesk bin mail --update $email -outgoing-messages-mbox-limit 0 1> /dev/null && echo Outgoing email limit for $email set to 0"
        set sshStatus (echo $status)
        if test $sshStatus -eq 0
            echo I did
            echo "plesk bin mail -u $email -passwd '$password' && plesk bin mail --update $email -outgoing-messages-mbox-limit 0"
        end
        return $sshStatus
end
