call activate mmdmat || goto die
set TAG="ver1.02.01"
git clone --depth 1 -b %TAG% https://github.com/miu200521358/3d-pose-baseline-vmd.git || goto die
cd 3d-pose-baseline-vmd || goto die
mkdir data || goto die
cd data || goto die
curl -sc cookie "https://drive.google.com/uc?id=1W5WoWpCcJvGm4CHoUhfIB0dgXBDCEHHq&export=download" > log.txt || goto die
for /f "usebackq" %%t in (`awk '/_warning_/ {print $NF}' cookie`) do set TOKEN=%%t
set MSG1="https://drive.google.com/uc?export=download&confirm="
set MSG2="&id=1W5WoWpCcJvGm4CHoUhfIB0dgXBDCEHHq"
set URL=%MSG1%%TOKEN%%MSG2%
curl -Lb cookie %URL% -o h36m.zip || goto die
unzip h36m.zip || goto die
rm h36m.zip cookie log.txt || goto die
cd .. || goto die
curl -sc cookie "https://drive.google.com/uc?id=1v7ccpms3ZR8ExWWwVfcSpjMsGscDYH7_&export=download" > log.txt || goto die
for /f "usebackq" %%t in (`awk '/_warning_/ {print $NF}' cookie`) do set TOKEN=%%t
set MSG1="https://drive.google.com/uc?export=download&confirm="
set MSG2="&id=1v7ccpms3ZR8ExWWwVfcSpjMsGscDYH7_"
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
