function vlog --description 'Returns link to open given VDS in admin panel'
    set vpsHostName (echo $argv)
    set vpsID (curl -s "https://virtualizor.hoster.kz:4085/index.php?act=vs&vpshostname=$vpsHostName&api=json&adminapikey=$VZR_API_KEY&adminapipass=$VZR_API_PASS" | jello -lr '[f"{k}:{v}" for server_record in _.vs.values() for k,v in server_record.iteritems() if k=="vpsid"]' | string split ":" -f2 )
    echo "https://virtualizor.hoster.kz:4085/sessgqilzJrNIvhAFYoW/index.php?act=login&redirect=%2FsessgqilzJrNIvhAFYoW%2Findex.php%3F%26act%3Dmanagevps%26vpsid%3D$vpsID"
end
