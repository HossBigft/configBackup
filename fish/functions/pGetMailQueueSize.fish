function pGetMailQueueSize
    ls ~/pkzStats/pleskMailQueueSize*|tail -n 1|xargs cat;
end
