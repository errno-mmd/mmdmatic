call activate mmdmat || goto die
git clone --depth 1 -b mmdmatic https://github.com/errno-mmd/motion_trace_bulk.git || goto die

@echo COMPLETE
@pause -1
exit /b 0

:die
@echo ERROR
@pause -1
exit /b 1
