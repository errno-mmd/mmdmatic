call activate mmdmat || goto die
call conda install -y curl || goto die
call conda install -y git || goto die
call conda install -y cython || goto die
call conda install -y m2-base || goto die
call conda install -y m2-tar || goto die
call conda install -y m2-unzip || goto die
call conda install -y m2-gawk || goto die
call conda install -y swig || goto die
call conda install -y python-dateutil || goto die
call conda install -y pytz || goto die
call conda install -y pyparsing || goto die
call conda install -y six || goto die
call conda install -y matplotlib || goto die
call conda install -y opencv || goto die
call conda install -y imageio || goto die
call conda install -y h5py || goto die
call conda install -y pyqt || goto die
call conda install -y dill || goto die
call conda install -y numba || goto die
call conda install -y psutil || goto die
call conda install -y requests || goto die
call conda install -y scikit-image || goto die
call conda install -y scipy || goto die
call conda install -y tqdm || goto die
call conda install -y pillow==6.2.1
pip install fire || goto die
pip install slidingwindow || goto die

@echo COMPLETE
@pause -1
exit /b 0

:die
@echo ERROR
@pause -1
exit /b 1
