function pMailTestCreate --wraps=ssh
    set host (echo $argv[1])
    set domain (echo $argv[2])
    set testMail "testhostermail"
    set password (pwgen | string split " " -f1)
    ssh maximg@$host "plesk bin mail --create $testMail@$domain -passwd \"$password\" -mailbox true -description \"$password\""
    printf $password"\n"
end
