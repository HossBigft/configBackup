function digsx
    if test (count $argv) -eq 0
        return 1
    end
    if set answer (digs $argv)
        digs -x $answer
        return 0
    else
        echo no Result for $argv
        return 1
    end
end
