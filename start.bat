@echo off

rem ===== Settings =====
set INTERVAL=3
set REPO=
rem =====================
rem REPO examples:
rem   set REPO=C:\Users\User\Documents\dev\repos\my-project
rem   set REPO=.
rem Leave empty to run without commit detection

if "%REPO%"=="" (
    python "%~dp0auto_alt_enter.py" --interval %INTERVAL%
) else (
    python "%~dp0auto_alt_enter.py" --interval %INTERVAL% --repo "%REPO%"
)
pause
