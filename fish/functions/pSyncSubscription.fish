function pSyncSubscription --wraps=ssh --description 'Unlocks and syncs given subscription on given server'

set argNum (count $argv)

    if test $argNum -eq 2
        set subscription_name (echo $argv[2])
        set host (echo $argv[1])
    else
        echo Wrong number of arguments
        return 1
    end

    
    ssh $host "plesk bin subscription --unlock-subscription  $subscription_name && plesk bin subscription --sync-subscription $subscription_name"
    return 0
end
