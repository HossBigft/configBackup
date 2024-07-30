function pQueryMailQueueSize
    set currDate (date +%Y%m%d_%H%M)
    set filename pleskMailQueueSize
    set servers (cat ~/.ssh/config|grep -Po "(?<=Hostname ).*|(?<=HostName ).*"|grep -Pv "ns.*hoster.kz|((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}")

    
    echo "Starting queries"
    mkdir -p ~/pkzStats && touch ~/pkzStats/$filename$currDate.txt
    
    for server in $servers
        echo "Querying $server"
        set response (ssh maximg@$server "mailq | grep -c '^[A-F0-9]'")
        echo "$server  answered $response"
        echo $server\; Mail queue size $response >>~/pkzStats/$filename$currDate.txt
    end
    
    echo Sorting
    sort -t' ' -n -k5 -o ~/pkzStats/$filename$currDate.txt{,}
    echo "Saved in ~/pkzStats/$filename$currDate.txt"
end
