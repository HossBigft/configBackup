function digsx
    if set answer (digs $argv)
        digs -x $answer
        return 0
    else
        echo no Result for $argv
        return 1
    end
end
