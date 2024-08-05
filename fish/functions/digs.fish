function digs
    set argsLen (count $argv)
    set ipRegexPattern "((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}"
    
    if test $argsLen -eq 1 
        if string match -qr $ipRegexPattern $argv
            printf $argv
            return 0
        end
        set answer (dig +short @8.8.8.8  $argv)
        if test -n "$answer"
            printf %s\n  $answer
            return 0
        else
            echo No result for $argv
            return 1
        end
    else
        set answer (dig +short  $argv)
        if test -n "$answer"
            printf %s\n  $answer
            return 0
        else
            echo No result for $argv
            return 1
        end
    end
end
