function pCheckMigrationVersion
    set targetVersion (echo $argv[1])
    echo $targetVersion
    set subscriptionSize (echo $argv[2])
    set listOfVersionCompatibleServer (fish -c pFindSameVersionOrGreater|echo $targetVersion|psub)
    echo $listOfVersionCompatibleServer
end
