#!/bin/bash
# concatenate all .jpg to 1 multipage pdf in a4 format

convert *.jpg -compress jpeg -resize 1240x1753 -extent 1240x1753 -gravity center -units PixelsPerInch -density 150x150 multipage.pdf

gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/screen -dNOPAUSE -dQUIET -dBATCH -sOutputFile=multipage_shrinked.pdf multipage.pdf
