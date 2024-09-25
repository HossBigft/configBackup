function nsZoneMaster --description "Returns zone master value from DNS servers for given domain. Can return only ip with -q/--quiet option"
  python3 /home/gmv/configBackup/pyScrs/nsZoneMaster.py $argv
end
