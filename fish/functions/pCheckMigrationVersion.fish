function pCheckMigrationVersion
    set targetVersion (echo $argv[1])
    set subscriptionSize (echo $argv[2])
    set listOfVersionCompatibleServers (fish -c "pFindSameVersionOrGreater $targetVersion" | grep -Po "^([^|])+")
    set listOfSpaceFittingServers (fish -c "pCheckMigrationSpace $subscriptionSize")
    echo $listOfVersionCompatibleServers
    echo $listOfSpaceFittingServers
end
