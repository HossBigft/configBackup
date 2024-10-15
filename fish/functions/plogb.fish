function plogb --wraps=ssh --description 'generates link to open plesk backup manager of given server'
    set host (echo $argv[1])
    
    set redirectionHeader "&success_redirect_url=%2Fadmin%2Fbackup%2Flist%2Fd"
    set loginLink (plog $host)
    if test $status -eq 1
        echo "Login link generation for $host failed"
        return 1
    end
    echo $loginLink$redirectionHeader
    return 0
end
