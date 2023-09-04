@echo off
title ROD - Install
call runtime\Scripts\activate
call runtime\Scripts\python -m pip uninstall -y -r install.txt
call runtime\Scripts\python -m pip install -r install.txt
echo.
echo PACKAGES INSTALLED
pause