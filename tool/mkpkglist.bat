call conda activate mmdmat
call conda list -e | grep -v pypi | grep -v torch > condapkglist.txt
call conda list -e | grep pypi | sed -e 's/=pypi_0//' | sed -e 's/=/==/' > pypipkglist.txt
call conda list -e | grep torch > torchpkglist.txt
