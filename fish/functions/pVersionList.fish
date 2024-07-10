function pVersionList
    for i in (cat ~/.ssh/config|grep -Po "(?<=Hostname ).*|(?<=HostName ).*"|grep -Pv "ns.*hoster.kz|^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}\$")
        set pleskVersion (ssh maximg@$i 'plesk -v'|grep -Po "Plesk.*");
        echo $i $pleskVersion;
    end;
end
