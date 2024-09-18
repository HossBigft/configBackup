function _pDomainToCageFsUsername
    set argNum (count $argv)

    if test $argNum -eq 1
        string shorten -m12 -c "" $argv | string replace -ar "\." "_"
    else
        echo Too much arguments
    end
end
