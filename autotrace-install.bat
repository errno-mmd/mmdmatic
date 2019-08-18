call activate autotracevmd

call package-install.bat

call tfpose-install.bat
cd /d %~dp0

call FCRN-install.bat
cd /d %~dp0

call 3dpose-install.bat
cd /d %~dp0

call VMD3d-install.bat
cd /d %~dp0

pause -1
