function pQueryMailmanVersion
    set currDate (date +%Y%m%d_%H%M)
    set filename pleskMailmanVersions
    set pleskServers (cat ~/.ssh/config|grep -Po "(?<=Hostname ).*|(?<=HostName ).*"|grep -Pv "ns.*hoster.kz|^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}\$")

    echo "Starting query {rpm -q mailman}"

    mkdir -p ~/pkzStats && touch ~/pkzStats/$filename$currDate.txt

    for host in $pleskServers
        set ver (ssh maximg@$host 'rpm -q mailman')
        echo $host $ver
        echo $host $ver >> ~/pkzStats/$filename$currDate.txt
    end
    
    echo Sorting
    sort -t' ' -k2 -o ~/pkzStats/$filename$currDate.txt{,}

    echo "Saved in ~/pkzStats/$filename$currDate.txt"
end
