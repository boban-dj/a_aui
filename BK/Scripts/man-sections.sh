!/bin/sh
MANPAGER=cat man $@ | grep -E '^^[[1m[A-Z]{3,}'
