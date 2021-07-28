@REM @Author: CPS
@REM @email: 373704015@qq.com
@REM @Date:
@REM Last Modified by: CPS
@REM Last Modified time: 2021-07-23 15:15:17.858789
@REM Modified time: 2021-07-23 15:15:17.858789
@REM @file_path "Z:\CPS\MyProject\mikepy"
@REM @Filename "open-jupyterNotebook-with-currtDir.bat"

@echo off

@rem %~dp0 当前目录
@rem --NotebookApp.ip 允许所有ip访问，适用于开发环境，局域网调试
@rem --NotebookApp.token 完全取消权限验证，开发环境不需要验证，也可以指定某个token，固定
@rem --NotebookApp.port 指定端口

@:: surface pro7
@if "%COMPUTERNAME%" == "DESKTOP-49G127I" (@set "notebook=D:\CPS\python\Python375_64\Scripts\jupyter-notebook.exe"&goto start-notebook)

@:: home-pc
@if "%COMPUTERNAME%" == "home" (@set "notebook=Z:\CPS\python\Python375_64\Scripts\jupyter-notebook.exe"&goto start-notebook)

@:: 办公室电脑
@if "%COMPUTERNAME%" == "DESKTOP-S9VGC7V" (@set "notebook=Z:\CPS\python\Python375_64\Scripts\jupyter-notebook.exe"&goto start-notebook)


exit

:start-notebook
@%notebook% %~dp0 --NotebookApp.port=4444 --NotebookApp.ip=* --NotebookApp.token=''
