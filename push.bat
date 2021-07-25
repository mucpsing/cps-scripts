::git add ./server/*
::git add ./admin/*

@if "%COMPUTERNAME%" == "DESKTOP-49G127I" (@set "client=surfacePro7")

git add .
git commit -m "%client% fast push"
git push origin master
pause