echo off
set key=%1
set sig=%2
set file=%3
openssl dgst -sha256 -verify %key% -signature %sig% %file%