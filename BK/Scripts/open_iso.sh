#!/bin/bash
# open-iso.sh
# mount .iso file in new folder, unmount if mounted already
# requires fuseiso and libnotify-bin (for notify-send messages)

shopt -s nocasematch
[[ -f $1 ]] && [[ $1 =~ \.(iso|bin|mdf|img|nrg)$ ]] ||  { notify-send "open-iso.sh" "$1 is not a supported file type"; exit 1 ;}
shopt -u nocasematch
foldername=${1}.mount
if grep "^fuseiso[[:space:]]$(readlink -f $foldername)" /etc/mtab >/dev/null
then
	fusermount -u "$foldername" || { notify-send "open-iso.sh" "failed to unmount $1"; exit 1;}
	notify-send "open-iso.sh" "$1 has been unmounted"
else
	[[ -d $foldername ]] && [[ $( ls -A $foldername ) ]] && { notify-send "open-iso.sh" "$foldername is not empty" ; exit 1 ;}
    fuseiso -p "$1" "$foldername" || { notify-send "open-iso.sh" "failed to mount $1"; exit 1;}
    notify-send "open-iso.sh" "$1 has been mounted on $foldername"
fi

exit
