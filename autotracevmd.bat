@echo off

call conda --version && goto :confcheck

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

:confcheck
if not exist tool\config.json (
    echo Config file is not exist.
    echo Run setup before running autotrace.
    exit /b 1
)

call conda activate --no-stack mmdmat || goto die
set TF_FORCE_GPU_ALLOW_GROWTH=true
cd tool && start pythonw gui_autotrace.py && cd .. || goto die
call conda deactivate
exit /b 0

:die
@echo ERROR
@pause -1
exit /b 1