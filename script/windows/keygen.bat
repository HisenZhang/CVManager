echo off
set keyname=%1
openssl genrsa -out %keyname%_private.pem
openssl rsa -in %keyname%_private.pem -pubout -out %keyname%_public.pem