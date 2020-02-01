call activate mmdmat || goto die
set TAG="ver1.03"
git clone --depth 1 -b %TAG% https://github.com/miu200521358/mannequinchallenge-vmd.git || goto die
cd mannequinchallenge-vmd || goto die
bash fetch_checkpoints.sh || goto die
bash fetch_davis_data.sh || goto die

@echo COMPLETE
@pause -1
exit /b 0

:die
@echo ERROR
@pause -1
exit /b 1

