call activate mmdmat || goto die
git clone --depth 1 https://github.com/errno-mmd/tf-pose-estimation.git || goto die
cd tf-pose-estimation || goto die
cd tf_pose\pafprocess || goto die
swig -python -c++ pafprocess.i || goto die
python setup.py build_ext --inplace || goto die

@echo COMPLETE
@pause -1
exit /b 0

:die
@echo ERROR
@pause -1
exit /b 1

