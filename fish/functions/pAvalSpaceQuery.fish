function pAvalSpaceQuery
    set currDate (date +%Y%m%d_%H%M)
    set filename 'pleskAvailableSpace'
    echo "Starting queries"
    mkdir -p ~/pkzStats && touch ~/pkzStats/$filename$currDate.txt
    for i in (cat ~/.ssh/config|grep -Po "(?<=Hostname ).*|(?<=HostName ).*"|grep -Pv "ns.*hoster.kz|^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}\$")
        set avalSpace (ssh maximg@$i 'df -h'|grep -P ".*\/\$")
        echo $i $avalSpace
        echo $i $avalSpace|tr -s ' '  >> ~/pkzStats/$filename$currDate.txt
    end
    echo "Sorting"
    sort -t' ' -k6 -r -o ~/pkzStats/$filename$currDate.txt{,}
    echo "Saved in ~/pkzStats/$filename$currDate.txt"
end
