function pQueryMailQueueSize
    set  filename "pleskMailQueueSize"
    set  currDate (date +%Y%m%d_%H%M)

    
    python3.12 /home/gmv/configBackup/pyScrs/pQuery.py $filename "mailq | grep -c '^[A-F0-9]'"
    
    echo Sorting..
    set filePath (ls ~/pkzStats/$filename* | tail -n 1)
    sort -t'|' -n -k2  --output (ls ~/pkzStats/$filename* | tail -n 1){,}
    echo "Sorted file saved in $filepath"
end
