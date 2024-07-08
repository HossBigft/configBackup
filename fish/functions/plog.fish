function plog --wraps=ssh
    ssh $argv 'plesk login'
end
