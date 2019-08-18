call activate autotracevmd
git clone --depth 1 https://github.com/miu200521358/FCRN-DepthPrediction-vmd.git
cd FCRN-DepthPrediction-vmd\tensorflow
mkdir data
cd data
curl -L -O http://campar.in.tum.de/files/rupprecht/depthpred/NYU_FCRN-checkpoint.zip
unzip NYU_FCRN-checkpoint.zip
rm NYU_FCRN-checkpoint.zip
