function pPhpMailToggle --wraps=ssh
    set argNum (count $argv)

    if test $argNum -eq 1
        set domain (echo $argv[1])
        set host (_findPleskHost $domain)
        if test $status -eq 1
            echo "Host for $domain was not found"
            return 1
        else
            echo "Host for $domain is $host"
        end
    else if test $argNum -eq 2
        set host (echo $argv[1])
        set domain (echo $argv[2])
    end
    ssh $host "domain=$domain; phpIniPath=/var/www/vhosts/system/\$domain/etc/php.ini;
    if [ -f \$phpIniPath ]; then
        if grep -qP \"disable_functions =.*mail\" \$phpIniPath;then
            sed -i '/^disable_functions =/s/,mail//g' \$phpIniPath && plesk bin site --update-php-settings \$domain  -settings \$phpIniPath;
            
            echo \"\$domain: PHP mail is enabled\";
        else
            sed -i 's/^\(disable_functions = \".*\)\"\$/\1,mail\"/' \$phpIniPath && plesk bin site --update-php-settings \$domain -settings \$phpIniPath;
    
            printf \"%s: PHP mail is disabled. Execute commands below to enable it back: \nsed -i '/^disable_functions =/s/,mail//g' %s && plesk bin site --update-php-settings %s -settings %s\n\" \$domain \$phpIniPath \$domain \$phpIniPath;
        fi;
    else
     echo \$domain does not exist
    fi"
end
