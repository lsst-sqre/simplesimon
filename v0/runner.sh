#!/usr/bin/env bash
workdir="${HOME}/ci_work/$(date +'%Y-%m-%d')"
mkdir -p ${workdir}
cd ${workdir}
unset DEBUG
curl -s -L -O https://raw.githubusercontent.com/lsst-sqre/notebook-demo/master/$1.ipynb
FILE=$(basename "$1")
# This should not depend on user setups
jupyter-nbconvert --to notebook --execute --output ${FILE}_out.ipynb --ExecutePreprocessor.timeout=$2 ${FILE}.ipynb
