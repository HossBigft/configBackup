function pMailmanVersionList
    set currDate (date +%Y%m%d_%H%M)
    echo "Starting queries"
    mkdir -p ~/pkzStats && touch ~/pkzStats/pleskMailmanVersions$currDate
    for i in (cat ~/.ssh/config|grep -Po "(?<=Hostname ).*|(?<=HostName ).*"|grep -Pv "ns.*hoster.kz|^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}\$")
        set ver (ssh maximg@$i 'rpm -q mailman')
        echo $i $ver
        echo $i $ver >> ~/pkzStats/pleskMailmanVersions$currDate.txt
    end
    echo "Saved in ~/pkzStats/pleskMailmanVersions$currDate.txt"
end
