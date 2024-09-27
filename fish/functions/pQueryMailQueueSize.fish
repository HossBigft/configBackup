function pQueryMailQueueSize
    set  filename "pleskMailQueueSize"
    set  currDate (date +%Y%m%d_%H%M)
    set scriptsPath (find ~ -maxdepth 1 -name configBackup  | head -n1)
    
    python3.12  $scriptsPath/pyScrs/pQuery.py $filename "mailq | grep -c '^[A-F0-9]'"
    
    echo Sorting..
    sort -t'|' -n -k2  --output (ls ~/pkzStats/$filename* | tail -n 1){,}
    echo "Sorted file saved in "(ls ~/pkzStats/$filename* | tail -n 1)
end
