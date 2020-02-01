call activate mmdmat || goto die
set TAG="ver1.03"
git clone --depth 1 -b %TAG% https://github.com/miu200521358/VMD-3d-pose-baseline-multi.git || goto die

@echo COMPLETE
@pause -1
exit /b 0

:die
@echo ERROR
@pause -1
exit /b 1
