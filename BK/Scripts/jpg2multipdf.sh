#!/bin/bash
## Concatenate all .jpg to 1 multipage pdf in a4 format
## Some quality loss

convert *.jpg -compress jpeg -resize 1240x1753 -extent 1240x1753 -gravity center -units PixelsPerInch -density 150x150 multipage.pdf
