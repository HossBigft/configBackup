function pPhpCageFsUserRestart --wraps=ssh --description 'Restarts CageFS user for given subscription. Takes server hostname, name of subscription or can take only name of subscription and try to find host'
 set argNum (count $argv)

    if test $argNum -eq 1
        set domain (echo $argv)
        set username (_pDomainToCageFsUsername $domain)
        set host (_findPleskHost $domain)
        if test $status -eq 1
            echo "Host for $domain was not found"
            return 1
        else
            echo "Host for $domain is $host"
        end
    else if test $argNum -eq 2
        set domain (echo $argv[2])
        set username (_pDomainToCageFsUsername $domain)
        set host (echo $argv[1])
    end
    ssh $host "echo Initial status: User $username is \$(cagefsctl --user-status $username)&& cagefsctl --disable $username && echo User $username is \$(cagefsctl --user-status $username) && cagefsctl --enable $username && echo User $username is \$(cagefsctl --user-status $username)"
end
