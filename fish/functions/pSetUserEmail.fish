function pSetUserEmail --wraps=ssh --description 'Set email of given user to given string'
 set argNum (count $argv)

    if test $argNum -eq 3
        set user (echo $argv[2])
        set host (echo $argv[1])
        set email (echo $argv[3])
    else
        echo Wrong input
        return 1
    end
    ssh $host "echo Email before update \$(plesk bin customer --info $user | grep Email | tr -s ' ' | awk '{print \$2}') && plesk bin customer -u $user -email $email && echo Email after update \$(plesk bin customer --info $user | grep Email | tr -s ' ' | awk '{print \$2}')"
    
end
