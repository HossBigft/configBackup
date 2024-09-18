function _pDomainToCageFsUsername
    set -l options r/reverse
    argparse -n _pDomainToCageFsUsername $options -- $argv
    set argNum (count $argv)

    if test $argNum -eq 2 || test $argNum -eq 1
        if  set -q _flag_reverse
         echo $argv | string replace -ar "_" "."
        else
            string shorten -m12 -c "" $argv | string replace -ar "\." "_"
        end
    else
        echo Too much arguments
    end
end
