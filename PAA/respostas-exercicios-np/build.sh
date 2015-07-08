#!/bin/bash
./clean.sh
pdflatex template
bibtex template
makeindex template.idx
makeglossaries template
wait
pdflatex template
makeglossaries template
wait
pdflatex template
evince template.pdf
