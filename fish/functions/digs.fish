function digs
    set argsLen (count $argv)
    if test $argsLen -eq 1 
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
