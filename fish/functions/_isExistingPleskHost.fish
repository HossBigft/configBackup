function _isExistingPleskHost --wraps=ssh --description 'Returns 0 if there is existing plesk host'
    grep -P "^Host ([^*]+)\$" $HOME/.ssh/config | sed 's/Host //'|grep -- p-| grep -wq $argv
    
set lastCmdExectionStatus (echo $status)
return $lastCmdExectionStatus
end
