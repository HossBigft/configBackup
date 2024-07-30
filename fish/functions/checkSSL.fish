function checkSSL
    nmap -p 443 --script ssl-cert $argv
end
