function pCheckMigrationVersion
    set targetVersion (echo $argv[1])
    set subscriptionSize (echo $argv[2])
    set listOfVersionCompatibleServernames (fish -c "pFindSameVersionOrGreater $targetVersion" | grep -Po "^([^|])+")
    set listOfSpaceFittingServers (fish -c "pCheckMigrationSpace $subscriptionSize" )
    set listOfSpaceFittingServernames
    for line in $listOfSpaceFittingServers
        set -a listOfSpaceFittingServernames  (echo $line | grep -Po "^([^|])+")
    end
    set listOfVersionSpaceCompatibleServers  (echo $listOfSpaceFittingServers | grep -P (string join '|' $listOfVersionCompatibleServernames))
    for server in (string split ';' (string replace -a '; ' ';' $listOfVersionSpaceCompatibleServers))
        echo $server
    end
end
