function digs
    set argsLen (echo $argv|string length)
    
    if test $argsLen -eq 1 
        set answer (dig @8.8.8.8 +short $argv)
        if test -n "$answer"
            echo $answer
            return 0
        else
            echo No result for $argv
            return 1
        end
    else
        set answer (dig +short $argv)
        if test -n "$answer"
            echo $answer
            return 0
        else
            echo No result for $argv
            return 1
        end
    end
end
