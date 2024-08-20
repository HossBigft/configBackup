function digsx
    if test (count $argv) -eq 0
        return 1
    else if test (count $argv) -eq 1
        if set answer (digs $argv)
            digs -x $answer
            return 0
        else
            echo "no Result for $argv"
            return 1
        end
    else
        for ip in $argv
               echo (digs -x $ip)
        end
    end
end
