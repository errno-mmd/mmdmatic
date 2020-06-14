@echo off

echo mmdmatic uninstaller
echo All the packages and virtual environment mmdmatic installed will be removed.
choice /m "Are you sure you want to remove them?"
if %errorlevel% == 1 (goto :yes)
if %errorlevel% == 2 (goto :no)

:yes
call conda env remove -n mmdmat || goto die
@echo COMPLETE
@pause -1
exit /b 0

:no
echo Canceled
@pause -1
exit /b 0

:die
@echo ERROR
@pause -1
exit /b 1
