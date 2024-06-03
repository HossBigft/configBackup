function dwho --wraps='dig +short  | xargs whois'
dig +short $argv | head -n 1| xargs whois ; 
end
