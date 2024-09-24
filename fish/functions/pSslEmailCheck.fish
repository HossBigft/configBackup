function pSslEmailCheck --description "Returns data of certificate, which used for mail 465 connection"
 openssl s_client -showcerts -connect mail.$argv:465 -servername mail.$argv | openssl x509 -dates -noout; 
end
