function pGetDNSRecords --wraps=ssh
 ssh $argv[1] "plesk bin dns --info $argv[2]"|awk NF|head -n -1; 
end
