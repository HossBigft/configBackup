function pCheckMigrationVersion
    set targetVersion (echo $argv[1])
    set subscriptionSize (echo $argv[2])
    set listOfVersionCompatibleServers (fish -c "pFindSameVersionOrGreater $targetVersion")
    set listOfVersionCompatibleServernames (string collect $listOfVersionCompatibleServers | grep -Po "^([^|])+")
    set listOfSpaceFittingServers (fish -c "pCheckMigrationSpace $subscriptionSize")
    set listOfSpaceFittingServernames
    
    for line in $listOfSpaceFittingServers
        set -a listOfSpaceFittingServernames  (echo $line | grep -Po "^([^|])+")
    end
    
    set regexPatternForVersionCompatibleServerNames (string join '|' $listOfVersionCompatibleServernames)
    set listOfVersionSpaceCompatibleServers  (string split -n ';' $listOfSpaceFittingServers | grep -P $regexPatternForVersionCompatibleServerNames )
    
    for server in (string split -n ';' (string replace -a '; ' ';' $listOfVersionSpaceCompatibleServers))
        echo $server\;
    end
end
