function pCheckEmailSSL
 openssl s_client -showcerts -connect mail.$argv:465 -servername mail.$argv | openssl x509 -dates -noout; 
end
