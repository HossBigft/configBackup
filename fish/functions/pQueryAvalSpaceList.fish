function pQueryAvalSpaceList
    set currDate (date +%Y%m%d_%H%M)
    set filename pleskAvailableSpace
    set servers (cat ~/.ssh/config|grep -Po "(?<=Hostname ).*|(?<=HostName ).*"|grep -Pv "ns.*hoster.kz|((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}")

    python3.12 /home/gmv/configBackup/pyScrs/pQuery.py $filename "df -BG | tr -s ' '|sed ':a; N; \\\$!ba; s/\\\n/; /g'|grep -Po '(?:\\\S+\\s+){5}\\\/var;|((?:\\\S+\\\s+){5}\\\/;)(?!.*\\\/var;)'"
    
    echo Sorting
    sort -t' ' -k5 -r -o ~/pkzStats/$filename$currDate.txt{,}
    echo "Saved in ~/pkzStats/$filename$currDate.txt"
end
