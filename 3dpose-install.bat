call activate mmdmat || goto die
set TAG="mat1.03-3"
git clone --depth 1 -b %TAG% https://github.com/errno-mmd/3d-pose-baseline-vmd.git || goto die
cd 3d-pose-baseline-vmd || goto die
mkdir data || goto die
cd data || goto die
curl -L -O https://www.dropbox.com/s/e35qv3n6zlkouki/h36m.zip || goto die
unzip h36m.zip || goto die
rm h36m.zip || goto die
cd .. || goto die
curl -sc cookie "https://drive.google.com/uc?id=1SNeg6OhaE99OKB8GE6RDfSl3hnjnJ-K7&export=download" > log.txt || goto die
for /f "usebackq" %%t in (`awk '/_warning_/ {print $NF}' cookie`) do set TOKEN=%%t
set MSG1="https://drive.google.com/uc?export=download&confirm="
set MSG2="&id=1SNeg6OhaE99OKB8GE6RDfSl3hnjnJ-K7"
set URL=%MSG1%%TOKEN%%MSG2%
curl -Lb cookie %URL% -o experiments.zip || goto die
unzip experiments.zip || goto die
rm experiments.zip cookie log.txt || goto die

@echo COMPLETE
@pause -1
exit /b 0

:die
@echo ERROR
@pause -1
exit /b 1
