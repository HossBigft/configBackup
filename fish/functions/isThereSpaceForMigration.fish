function isThereSpaceForMigration
    set cleanString (echo $argv[1]| tr -s ' ')
    set total (echo $cleanString|string split -f 2 ' '|string sub -e -1)
    set used (echo $cleanString|string split -f 3 ' '|string sub -e -1)
    set added $argv[2]
    set usedPercentAfter (math ceil (math \(\($used+$added\)/$total\)\*100))
    if test $usedPercentAfter -ge 87
        echo "Not enough space --- used space will be $usedPercentAfter%"
    else
        echo $usedPercentAfter
    end
    
end
