call activate autotracevmd
git clone --depth 1 https://github.com/miu200521358/3d-pose-baseline-vmd.git
cd 3d-pose-baseline-vmd
mkdir data
cd data
curl -L -O https://www.dropbox.com/s/e35qv3n6zlkouki/h36m.zip
unzip h36m.zip
rm h36m.zip
cd ..
curl -sc cookie "https://drive.google.com/uc?id=1v7ccpms3ZR8ExWWwVfcSpjMsGscDYH7_&export=download" > log.txt
for /f "usebackq" %%t in (`awk '/_warning_/ {print $NF}' cookie`) do set TOKEN=%%t
set MSG1="https://drive.google.com/uc?export=download&confirm="
set MSG2="&id=1v7ccpms3ZR8ExWWwVfcSpjMsGscDYH7_"
set URL=%MSG1%%TOKEN%%MSG2%
curl -Lb cookie %URL% -o experiments.zip
unzip experiments.zip
rm experiments.zip cookie log.txt
