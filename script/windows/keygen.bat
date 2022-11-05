echo off
set keyname=%1
openssl genrsa -out %keyname%_key_private.pem
openssl rsa -in %keyname%_key_private.pem -pubout -out %keyname%_key_public.pem