#!/bin/bash
 
FILE=$(basename "$1")
MOUNTPOINT="$HOME/Desktop/$FILE"
 
fusermount -u "$MOUNTPOINT"
