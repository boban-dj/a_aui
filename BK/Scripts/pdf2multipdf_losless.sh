#!/bin/bash
## Concatenate all .pdf to 1 multipage pdf in a4 format
## No quality loss

#convert *.pdf -compress jpeg -resize 1240x1753 -extent 1240x1753 -gravity center -units PixelsPerInch -density 150x150 multipage.pdf

#gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/printer -dNOPAUSE -dQUIET -dBATCH -sOutputFile=multipage_shrinked.pdf multipage.pdf

gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -sOutputFile=multiple.pdf *.pdf
