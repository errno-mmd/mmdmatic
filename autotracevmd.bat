@echo off
call conda --version
if %errorlevel% neq 0 (
    echo Anaconda is not installed or broken.
    echo ReInstall Anaconda first, then retry setup.
)

call conda activate mmdmat || goto die
start /min "" cmd /c python gui_autotrace.py
exit /b 0

:die
@echo ERROR
@pause -1
exit /b 1