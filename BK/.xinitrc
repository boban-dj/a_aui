#!/bin/sh

userresources=$HOME/.Xresources
usermodmap=$HOME/.Xmodmap
sysresources=/etc/X11/xinit/.Xresources
sysmodmap=/etc/X11/xinit/.Xmodmap

# merge in defaults and keymaps

if [ -f $sysresources ]; then

    xrdb -merge $sysresources

fi

if [ -f $sysmodmap ]; then
    xmodmap $sysmodmap
fi

if [ -f "$userresources" ]; then


    xrdb -merge "$userresources"

fi

if [ -f "$usermodmap" ]; then
    xmodmap "$usermodmap"
fi



# start some nice programs

if [ -d /etc/X11/xinit/xinitrc.d ] ; then
 for f in /etc/X11/xinit/xinitrc.d/?*.sh ; do
  [ -x "$f" ] && . "$f"
 done
 unset f
fi

#twm &
#xclock -geometry 50x50-1+1 &
#xterm -geometry 80x50+494+51 &
#xterm -geometry 80x20+494-0 &
#exec xterm -geometry 80x66+0+0 -name login




# Make sure this is before the 'exec' command or it won't be sourced.
[ -f /etc/xprofile ] && source /etc/xprofile
[ -f ~/.xprofile ] && source ~/.xprofile

# sourcing multiple files from ~/.Xresources.d
# this is included in ~/.Xresources
xrdb -I$HOME ~/.Xresources

# exec gnome-session
# exec startkde
#exec i3



# From arch wiki https://wiki.archlinux.org/index.php/Xinitrc#Making_a_DE.2FWM_choice
# Here Xfce is kept as default
#session=${1:-xfce}
#session=${1:-i3}

#case $session in
#    awesome           ) exec awesome;;
#    bspwm             ) exec bspwm;;
#    catwm             ) exec catwm;;
#    cinnamon          ) exec cinnamon-session;;
#    dwm               ) exec dwm;;
#    enlightenment     ) exec enlightenment_start;;
#    ede               ) exec startede;;
#    fluxbox           ) exec startfluxbox;;
#    gnome             ) exec gnome-session;;
#    gnome-classic     ) exec gnome-session --session=gnome-classic;;
#    i3|i3wm           ) exec i3;;
#    icewm             ) exec icewm-session;;
#    jwm               ) exec jwm;;
#    kde               ) exec startkde;;
#    mate              ) exec mate-session;;
#    monster|monsterwm ) exec monsterwm;;
#    notion            ) exec notion;;
#    openbox           ) exec openbox-session;;
#    unity             ) exec unity;;
#    xfce|xfce4        ) exec startxfce4;;
#    xmonad            ) exec xmonad;;
#    # No known session, try to run it as command
#    *) exec $1;;
#esac

exec startxfce4
