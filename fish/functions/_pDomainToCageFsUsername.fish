function _pDomainToCageFsUsername --description "Find CageFS user name by host and subscription name"
    set argNum (count $argv)

    if test $argNum -eq 2
        set subscriptionName (echo $argv[2])
        set host (echo $argv[1])
        ssh  $host "stat -c '%U %G' /var/www/vhosts/$subscriptionName/| awk '{print \$1}'"
        return $status
    else
        echo Too much arguments\[$argNum\]
        return 1
    end
end
