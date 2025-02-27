function plogPMG --wraps=ssh --description 'generates link to proxmox mail gateway panel'
     set pleskHost (echo $argv[1])
    
    set pmgHost (ssh $pleskHost "postconf -h relayhost | grep -Po '(?<!\.)\b[\w\-]+\.[\w\-]+\.\w+\b(?!\.)'")
    if test $status -ne 0
        echo "Proxmox Mail Gateway host retrieval for $host failed"
        return 1
    end
    echo "https://$pmgHost:8006/"
    return 0

end
