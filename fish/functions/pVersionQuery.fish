function pVersionQuery
    set currDate (date +%Y%m%d_%H%M)
    set filename pleskServerVersionList
    echo "Starting queries"
    mkdir -p ~/pkzStats && touch ~/pkzStats/$filename$currDate.txt
    for i in (cat ~/.ssh/config|grep -Po "(?<=Hostname ).*|(?<=HostName ).*"|grep -Pv "ns.*hoster.kz|^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}\$")
        set pleskVersion (ssh maximg@$i 'plesk -v'|grep -Po "Plesk.*")
        echo $i $pleskVersion
        echo $i $pleskVersion >> ~/pkzStats/$filename$currDate.txt
    end
    echo "Sorting by version"
    sort -k4 -o ~/pkzStats/$filename$currDate.txt{,}
    echo "Saved in ~/pkzStats/$filename$currDate.txt"
end
