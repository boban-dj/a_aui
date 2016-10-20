#
# ~/.bash_profile
#

[[ -f ~/.bashrc ]] && . ~/.bashrc



export PATH="$HOME/.rbenv/bin:$PATH"
eval "$(rbenv init -)"


source ~/perl5/perlbrew/etc/bashrc

export PATH="$HOME/.node_modules_global/bin:$PATH"

[[ -z $DISPLAY && $XDG_VTNR -eq 1 ]] && exec startx
