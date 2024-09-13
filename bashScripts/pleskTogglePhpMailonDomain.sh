domain=nodejs.gruzo.kz; phpIniPath=/var/www/vhosts/system/$domain/etc/php.ini;
if [ -f $phpIniPath ]; then
    if grep -qP "disable_functions =.*mail" $phpIniPath;then
        sed -i '/^disable_functions =/s/,mail//g' $phpIniPath && plesk bin site --update-php-settings $domain  -settings $phpIniPath
        echo "$domain: PHP mail is enabled"
    else
        sed -i 's/^\(disable_functions = ".*\)"$/\1,mail"/' $phpIniPath && plesk bin site --update-php-settings $domain -settings $phpIniPath

        printf "%s: PHP mail is disabled. \nExecute commands below to enable it back: \nsed -i '/^disable_functions =/s/,mail//g' %s && plesk bin site --update-php-settings %s -settings %s\n" $domain $phpIniPath $domain $phpIniPath
    fi;
fi;