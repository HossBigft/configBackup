function dwhom
 set mxRecord (digs mx $argv|string split " " -f2)
 digs $mxRecord|xargs whois
end
