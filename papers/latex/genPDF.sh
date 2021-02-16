#!/bin/sh

#./del_itm.sh

set -eu
touch m5231142.pdf
rm m5231142.pdf
set +e

latexmk -pdf m5231142.tex
# The error "I couldn't open file name `ref.aux'" happens,
# but ignore it because generating references is successful.