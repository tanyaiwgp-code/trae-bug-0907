@echo off
chcp 65001 >nul

REM 尝试使用指定路径的Python启动HTTP服务器
if exist "D:\Pyhon\python.exe" (
    echo 正在使用D:\Pyhon文件夹中的Python启动HTTP服务器...
    "D:\Pyhon\python.exe" -m http.server 8000
    pause
    exit
)

REM 尝试使用系统中的Python启动HTTP服务器
where python >nul 2>nul
if %errorlevel% equ 0 (
    echo 正在使用系统中的Python启动HTTP服务器...
    python -m http.server 8000
    pause
    exit
)

REM 如果没有Python，直接打开游戏文件
start "" "2048.html"

REM 显示说明
cls
echo 2048游戏说明:
echo 1. 如果您的默认浏览器已经打开了游戏，请在浏览器中访问它。
echo 2. 如果没有打开，请手动双击2048.html文件来启动游戏。
echo 3. 游戏操作: 使用方向键移动方块，相同数字的方块相撞时会合并。
echo 4. 目标: 尝试获得2048方块!
echo.
echo 按任意键退出...
pause >nul