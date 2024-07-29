function LEGACY_pFindSuitableServer
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
    set listOfCompatibleServers (string split -n ';' $listOfSpaceFittingServers | grep -Pw $regexPatternForVersionCompatibleServerNames )
    
    set listOfCompatibleServerNames ( string collect $listOfCompatibleServers | grep -Po "^([^|])+" )
    set listOfCompatibleVersions (string collect $listOfVersionCompatibleServers | grep -Pw (string join '|' $listOfCompatibleServerNames) | grep -Po "\d+(\.\d+)+ >= \d+(\.\d+)+;")


    set counter 1
    for server in (string split -n ';' (string replace -a '; ' ';' $listOfCompatibleServers))
        echo $server S\>\=T $listOfCompatibleVersions[$counter]
        set counter (math $counter+1)
    end
end
