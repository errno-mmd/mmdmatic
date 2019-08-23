call conda create -n mmdmat || goto die
call activate mmdmat || goto die
call conda install -y tensorflow-gpu || goto die
python tftest1.py || goto die

@echo COMPLETE
@pause -1
exit /b 0

:die
@echo ERROR
@pause -1
exit /b 1
