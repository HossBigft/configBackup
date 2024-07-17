function pFindSameVersionOrGreater
    set targetVersion (echo $argv)
    set targetVersionNumber (echo $targetVersion | string split '.' | string join '')
    set serverData (fish -c pGetVersionsList)

    for server in $serverData
        set serverVersion (echo $server | grep -Po "\d+(\.\d+)+")
        set serverVersionNumber (echo $serverVersion | string split '.' | string join '')
        if test $serverVersionNumber -ge $targetVersionNumber
            set serverName (echo $server | grep -Po "^([^.])+")
            echo $serverName\| $serverVersion \>\= $targetVersion
        end
    end
end
