call activate mmdmat || goto die
git clone --depth 1 https://github.com/errno-mmd/tf-pose-estimation.git || goto die
cd tf-pose-estimation || goto die
curl -L -O https://github.com/errno-mmd/tf-pose-estimation/releases/download/mmdmatic1.02.01/pycocotools.zip || goto die
unzip pycocotools.zip || goto die
cd tf_pose\pafprocess || goto die
curl -L -O https://github.com/errno-mmd/tf-pose-estimation/releases/download/mmdmatic1.02.01/_pafprocess.cp37-win_amd64.pyd || goto die

@echo COMPLETE
@pause -1
exit /b 0

:die
@echo ERROR
@pause -1
exit /b 1

