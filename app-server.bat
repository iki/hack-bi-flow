@echo off
setlocal
cd /d "%~dp0" || exit /b 1

set opts=app

if exist "app-secret.pem" set opts=%opts% --appidentity_email_address 568784795457-t1llbilkmq72e370hjdb5s063phmk749@developer.gserviceaccount.com --appidentity_private_key_path app-secret.pem

echo === dev_appserver.py %opts% >&2

dev_appserver.py %opts%
exit /b %errorlevel%
