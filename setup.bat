@echo off

call conda --version && goto :mkenv

set CONDAPATH=%HOMEPATH%\Anaconda3
set PATH=%CONDAPATH%\Scripts;%PATH%
set PATH=%CONDAPATH%\Library\bin;%PATH%
set PATH=%CONDAPATH%\Library\usr\bin;%PATH%
set PATH=%CONDAPATH%\Library\mingw-w64\bin;%PATH%
set PATH=%CONDAPATH%;%PATH%
call conda --version
if %errorlevel% neq 0 (
    echo Anaconda is not installed or broken.
    echo Install Anaconda first, then retry setup.
    exit /b 1
)

:mkenv
call conda install -y -n mmdmat python=3.7
if %errorlevel% == 0 goto pkginstall
call conda create --yes --force -n mmdmat python=3.7 || goto die

:pkginstall
call conda activate --no-stack mmdmat || goto die
call conda install -y wxpython requests conda || goto die

cd tool && start pythonw setup.py && cd .. || goto die
call conda deactivate
exit /b 0

:die
@echo ERROR
@pause -1
exit /b 1