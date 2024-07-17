function pCheckMigrationSpace
    set data (fish -c pGetAvalSpaceList)
    for line in $data
        set cleanString (echo $line| tr -s ' ')
        set host (echo $cleanString|string split -f 1 ' '|grep -Po "^([^.])+")
        set total (echo $cleanString|string split -f 3 ' '|string sub -e -1)
        set used (echo $cleanString|string split -f 4 ' '|string sub -e -1)
        set added $argv
        set newUsed (math $used+$added)
        
        set usedPercentAfter (math ceil (math \($newUsed/$total\)\*100))
        if test $usedPercentAfter -le 87
            echo $host\| New used space will be "$newUsed"G, new used percentage will be $usedPercentAfter%\;
        end
    end
end
