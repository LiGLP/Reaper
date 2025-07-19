@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

title Reaper Builder

:: Variables for plugin check and language menu
set plugins_installed=false

:language_menu
echo. 
echo ----------
echo (1) German
echo ----------
set /p lang=Choose Language: 
if "%lang%"=="1" (set lang=en) else if "%lang%"=="2" (set lang=de) else goto language_menu

:main_menu
cls
echo.
echo (1) Build
echo (2) Language Menu
echo.
set /p choice=Input: 
if "%choice%"=="1" goto build
if "%choice%"=="2" goto language_menu
goto main_menu

:build
cls
echo Do you want to build your Reaper? (Y/N)
set /p confirm=
if /I "%confirm%"=="J" goto extract
if /I "%confirm%"=="Y" goto extract
goto main_menu

:extract
cls
echo Extracting...
tar -xf packages.zip
if exist packages.zip del packages.zip

echo Installing plugins...
timeout /t 2 >nul

:: Check if plugins folder exists and install the tar.gz packages
if exist plugins (
    start cmd /c python -c "import os; os.system('pip show requests discord_webhook colored numpy || pip install plugins/colored-2.3.0.tar.gz plugins/discord_webhook-1.4.1.tar.gz plugins/numpy-2.2.4.tar.gz plugins/requests-2.32.3.tar.gz')"
    echo Plugins installed successfully.
    rmdir /s /q plugins
) else (
    echo No plugins to install. Skipping plugin installation...
)

echo Building Reaper...
timeout /t 5 >nul
start start.bat
exit
