call activate mmdmat || goto die
set TAG="ver1.02.01"
git clone --depth 1 -b %TAG% https://github.com/miu200521358/VMD-3d-pose-baseline-multi.git || goto die
cd VMD-3d-pose-baseline-multi\data || goto die
mkdir saved_sessions || goto die
cd saved_sessions || goto die
curl -L -O http://visual.cs.ucl.ac.uk/pubs/liftingFromTheDeep/res/init_session.tar.gz || goto die
tar zxvf init_session.tar.gz || goto die
rm init_session.tar.gz || goto die
curl -L -O http://visual.cs.ucl.ac.uk/pubs/liftingFromTheDeep/res/prob_model.tar.gz || goto die
tar zxvf prob_model.tar.gz || goto die
rm prob_model.tar.gz || goto die

@echo COMPLETE
@pause -1
exit /b 0

:die
@echo ERROR
@pause -1
exit /b 1
