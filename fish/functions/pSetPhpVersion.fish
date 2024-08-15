function pSetPhpVersion --wraps==ssh --wraps=ssh
    set host (echo $argv[1])
    set domain (echo $argv[2])
    set phpVersion (echo $argv[3])
    set availablePhpRegex "4.4|5.1|5.2|5.3|5.4|5.5|5.6|7.0|7.1|7.2|7.3|7.4|8.0|8.1|8.2|8.3"
    if string match -aqr $phpVersion $availablePhpRegex
        set username (echo $domain|string replace "." "_" )
        ssh maximg@$host "selectorctl --set-user-current=$phpVersion --user=$username"
        printf "Set PHP %s for user %s" $phpVersion $username
    else
        printf "Available PHP versions: $availablePhpRegex"
    end
end
