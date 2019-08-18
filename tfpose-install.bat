call activate autotracevmd
git clone --depth 1 https://github.com/errno-mmd/tf-pose-estimation.git
cd tf-pose-estimation
cd tf_pose\pafprocess
swig -python -c++ pafprocess.i
python setup.py build_ext --inplace
