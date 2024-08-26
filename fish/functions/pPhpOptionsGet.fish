function pPhpOptionsGet --wraps=ssh
    set host (echo $argv[1])
    set domain (echo $argv[2])
    set username (echo $domain|string replace -ra "\.|-" "_")
    
    ssh maximg@$host "curPHPVersion=\$(selectorctl --user-summary --user=$username|grep s|cut -d \" \" -f1);selectorctl  --print-options --version=\$curPHPVersion --user=$username --json" | jello -s|grep "\.value"| string replace "_.data." ""

end
