call activate autotracevmd

git clone --depth 1 https://github.com/miu200521358/VMD-3d-pose-baseline-multi.git
cd VMD-3d-pose-baseline-multi\data
mkdir saved_sessions
cd saved_sessions
curl -L -O http://visual.cs.ucl.ac.uk/pubs/liftingFromTheDeep/res/init_session.tar.gz
tar zxvf init_session.tar.gz
rm init_session.tar.gz
curl -L -O http://visual.cs.ucl.ac.uk/pubs/liftingFromTheDeep/res/prob_model.tar.gz
tar zxvf prob_model.tar.gz
rm prob_model.tar.gz
