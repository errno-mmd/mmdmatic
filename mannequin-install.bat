call activate mmdmat || goto die
set TAG="mat1.03.02"
git clone --depth 1 -b %TAG% https://github.com/errno-mmd/mannequinchallenge-vmd.git || goto die
cd mannequinchallenge-vmd || goto die
bash fetch_checkpoints.sh || goto die

@echo COMPLETE
@pause -1
exit /b 0

:die
@echo ERROR
@pause -1
exit /b 1

