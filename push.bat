::git add ./server/*
::git add ./admin/*

@if "%COMPUTERNAME%" == "DESKTOP-49G127I" (@set "client=surfacePro7")

@if "%COMPUTERNAME%" == "DESKTOP-S9VGC7V" (@set "client=office_win10")

git add .
git commit -m "%client% fast push"
git push origin master
pause