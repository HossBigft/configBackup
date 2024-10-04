function color_word
    set_color $argv[1]
    echo -n $argv[2]
    set_color normal
end
