function addSSHHost
    set -l options c/client p/private
    argparse -n addSSHHost $options -- $argv
    or return
    
    # Check if the correct number of arguments is provided
    if test (count $argv) -ne 2
        echo "Usage: add_ssh_host <user@host> <hostname>"
        return 1
    end

    # Parse the arguments
    set user_host $argv[1]
    set hostName $argv[2]

    # Extract username and host from the user_host argument
    set username (string split '@' $user_host)[1]
    set host (string split '@' $user_host)[2]
    set timeStamp (date +%Y%m%d_%H%M)
    if set -q _flag_private
        printf "#Added %s\nHost %s\n\tHostName %s\n\tUser %s\n\tIdentityFile ~/.ssh/id_rsa\n" $timeStamp  $hostName $host $username >> ~/.ssh/conf.d/private
        echo "Added host $hostName to private config"
        
    else if set -q _flag_client
        printf "#Added %s\nHost %s\n\tHostName %s\n\tUser %s\n\tIdentityFile ~/.ssh/id_rsa\n" $timeStamp  $hostName $host $username >> ~/.ssh/conf.d/clients
        echo "Added host $hostName to client config"
        
    else
        printf "#Added %s\nHost %s\n\tHostName %s\n\tUser %s\n\tIdentityFile ~/.ssh/id_rsa\n" $timeStamp  $hostName $host  $username >> ~/.ssh/config
        echo "Added host $hostName"
    end

end
