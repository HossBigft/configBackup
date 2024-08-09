function addSSHHost
    # Check if the correct number of arguments is provided
    if test (count $argv) -ne 2
        echo "Usage: addSSHHost <user@host> <hostname>"
        return 1
    end

    # Parse the arguments
    set user_host $argv[1]
    set hostName $argv[2]

    # Extract username and host from the user_host argument
    set username (string split '@' $user_host)[1]
    set host (string split '@' $user_host)[2]

    printf "Host %s\n\tHostName %s\n\tUser %s\n\tIdentityFile ~/.ssh/id_rsa\n" $host $hostName  $username >> ~/.ssh/config

    # Inform the user
    echo "Added new ssh host configuration for $hostName"
end
