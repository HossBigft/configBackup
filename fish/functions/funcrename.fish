function funcrename --wraps=funced
    set -l old_func $argv[1]
    set -l new_func $argv[2]
    if test $old_func = $new_func
        echo The function is alredy named $new_func
        return 1
    end

    set old_func_path (functions --details $old_func)
    set new_func_path (string replace -a $old_func $new_func $old_func_path)
    string replace -a $old_func $new_func (cat $old_func_path)>$new_func_path && rm $old_func_path
end
