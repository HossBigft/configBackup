function pGPHPVersion --wraps=ssh
    set host (echo $argv[1])
    set domain (echo $argv[2])
    set username (echo $domain|string replace "." "_")

    ssh maximg@$host "selectorctl --user-summary --user=$username|grep s|cut -d \" \" -f1"
end
