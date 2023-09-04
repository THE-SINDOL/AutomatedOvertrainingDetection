@echo off
title ROD - Tensorboard
setlocal enabledelayedexpansion

:: Define the path to the config.json file
set "config_file=config.json"

:: Read the "environment" value from the JSON file
for /f "tokens=2 delims=: " %%a in ('findstr /C:"\"environment\":" %config_file%') do (
    set "environment=%%~a"
    set "environment=!environment:"=!"  # Remove double quotes if present
    set "environment=!environment:,=!"  # Remove comma if present
)

:: Perform actions based on the environment value
if "!environment!"=="colab" (
    echo Running Colab Environment
    call runtime\Scripts\activate
    call runtime\Scripts\tensorboard.exe --logdir=%~dp0\logs\ --bind_all

) else if "!environment!"=="local" (
    echo Running Local Environment
    cd ..
    python -m tensorboard --logdir=%~dp0\logs\ --bind_all

) else (
    echo Invalid Environment %environment%
    pause
    exit /b
)

pause
endlocal
