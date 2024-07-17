function pCheckMigrationVersion
    set targetVersion (echo $argv[1])
    set subscriptionSize (echo $argv[2])
    set listOfVersionCompatibleServers (fish -c "pFindSameVersionOrGreater $targetVersion" | grep -Po "^([^|])+")
    set listOfSpaceFittingServers (fish -c "pCheckMigrationSpace $subscriptionSize" | tail -n +2)
    set listOfSpaceFittingServernames (echo $listOfSpaceFittingServers | grep -Po "^([^|])+")
    set listOfSpaceFittingServers (fish -c "pCheckMigrationSpace $subscriptionSize" | grep -Po "^([^|])+")
    set listOfVersionSpaceCompatibleServers (echo $listOfSpaceFittingServers | grep -Pw (echo $listOfSpaceFittingServernames | string join '|'))
    echo (echo $listOfSpaceFittingServernames | string join '|')
end
