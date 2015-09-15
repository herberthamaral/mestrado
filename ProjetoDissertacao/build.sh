#!/bin/bash
./clean.sh
pdflatex recordlinkage
bibtex recordlinkage
makeindex recordlinkage.idx
makeglossaries recordlinkage
wait
pdflatex recordlinkage
makeglossaries recordlinkage
wait
pdflatex recordlinkage
evince recordlinkage.pdf
