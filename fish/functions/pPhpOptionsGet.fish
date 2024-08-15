function pPhpOptionsGet --wraps=ssh
    set host (echo $argv[1])
    set domain (echo $argv[2])
    set username (echo $domain|string replace "." "_")
    
    ssh p-cloud-4 "selectorctl  --print-options --version=5.3 --user=$username --json"|jello -s|grep "\.value"| string replace "_.data." ""

end
