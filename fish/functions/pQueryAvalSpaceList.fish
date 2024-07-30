function pQueryAvalSpaceList
    set currDate (date +%Y%m%d_%H%M)
    set filename pleskAvailableSpace
    set servers (cat ~/.ssh/config|grep -Po "(?<=Hostname ).*|(?<=HostName ).*"|grep -Pv "ns.*hoster.kz|((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}")

    
    echo "Starting queries"
    mkdir -p ~/pkzStats && touch ~/pkzStats/$filename$currDate.txt
    
    for server in $servers
        echo "Querying $server"
        set response (ssh maximg@$server 'df -BG' | tr -s ' ' | string join "; " | grep -Po "(?:\S+\s+){5}\/var;|((?:\S+\s+){5}\/;)(?!.*\/var;)")
        echo "$server  answered $response"
        echo $server $response >>~/pkzStats/$filename$currDate.txt
    end
    
    echo Sorting
    sort -t' ' -k6 -r -o ~/pkzStats/$filename$currDate.txt{,}
    echo "Saved in ~/pkzStats/$filename$currDate.txt"
end
