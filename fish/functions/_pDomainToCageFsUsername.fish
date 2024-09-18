function _pDomainToCageFsUsername
    set -l options r/reverse
    argparse -n _pDomainToCageFsUsername $options -- $argv
    set argNum (count $argv)

    if test $argNum -le 2 
        if  set -q _flag_reverse
         echo $argv | string replace -ar "_" "."
        else
           string replace ".webspace" "" $argv | string shorten -m12 -c "" | string replace -ar "\." "_"
        end
        return 0
    else
        echo Too much arguments
        return 1
    end
end
