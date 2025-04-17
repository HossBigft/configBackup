function pMailCreateFromList --wraps=ssh --description 'Creates emails from a given file (one per line). Usage: pMailCreateFromList email_list.txt host'
    if test (count $argv) -ne 2
        echo "Usage: pMailCreateFromList email_list.txt host"
        return 1
    end

    set emailFile $argv[2]
    set host $argv[1]

    if not test -f "$emailFile"
        echo "File not found: $emailFile"
        return 1
    end

    set outputFile "created_emails.txt"
    echo -n > $outputFile

    for email in (cat "$emailFile" | string trim | grep -v '^#' | grep -v '^\s*$')
        set user (string split "@" $email)[1]
        set domain (string split "@" $email)[2]

        if test -z "$user" -o -z "$domain"
            echo "Invalid email format: $email"
            continue
        end

        set password (pwgen 20 | string split " " -f1)
        ssh $host "plesk bin mail --create $email -passwd '$password' -mailbox true"
        if test $status -eq 0
            echo "Created $email"
            echo "$email;$password;" >> $outputFile
        else
            echo "Failed to create $email"
        end
    end

    echo "Credentials saved to $outputFile"
end
