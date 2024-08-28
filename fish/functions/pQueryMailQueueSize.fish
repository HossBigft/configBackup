function pQueryMailQueueSize
    set  filename "pleskMailQueueSize"
    set  currDate (date +%Y%m%d_%H%M)
    set filePath ~/pkzStats/$filename$currDate.txt
    
    python3.12 /home/gmv/configBackup/pyScrs/pQuery.py $filename "mailq | grep -c '^[A-F0-9]'"
    
    echo Sorting..
    sort -t'|' -n -k2  --output $filePath{,}
    echo "Sorted file saved in $filePath"
end
