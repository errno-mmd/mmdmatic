@echo off
call conda --version
if %errorlevel% neq 0 (
    echo Anaconda is not installed or broken.
    echo Install Anaconda first, then retry setup.
)

call conda install -y -n mmdmat python=3.7
if %errorlevel% == 0 goto pkginstall
call conda create --yes --force -n mmdmat python=3.7 || goto die

:pkginstall
call conda activate mmdmat || goto die
call conda install -y wxpython requests conda || goto die

cd tool && start /min "" cmd /c python setup.py || goto die
exit /b 0

:die
@echo ERROR
@pause -1
exit /b 1