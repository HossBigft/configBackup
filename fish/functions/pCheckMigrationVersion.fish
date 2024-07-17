function pCheckMigrationVersion
    set targetVersion (echo $argv[1])
    set subscriptionSize (echo $argv[2])
    set listOfVersionCompatibleServer (fish -c "pFindSameVersionOrGreater $targetVersion")
    echo $listOfVersionCompatibleServer
end
