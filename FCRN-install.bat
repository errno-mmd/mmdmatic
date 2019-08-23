call activate mmdmat || goto die
set TAG="ver1.02.01"
git clone --depth 1 -b %TAG% https://github.com/miu200521358/FCRN-DepthPrediction-vmd.git || goto die
cd FCRN-DepthPrediction-vmd\tensorflow || goto die
mkdir data || goto die
cd data || goto die
curl -L -O http://campar.in.tum.de/files/rupprecht/depthpred/NYU_FCRN-checkpoint.zip || goto die
unzip NYU_FCRN-checkpoint.zip || goto die
rm NYU_FCRN-checkpoint.zip || goto die

@echo COMPLETE
@pause -1
exit /b 0

:die
@echo ERROR
@pause -1
exit /b 1
