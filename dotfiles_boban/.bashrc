################################################################################
## System related:
## overall_conditions, ps1, dircolors, exports, alias, dotfile extras
################################################################################


## OVERALL CONDITIONALS 
_islinux=false
[[ "$(uname -s)" =~ Linux|GNU|GNU/* ]] && _islinux=true

_isarch=false
[[ -f /etc/arch-release ]] && _isarch=true

_isxrunning=false
[[ -n "$DISPLAY" ]] && _isxrunning=true

_isroot=false
[[ $UID -eq 0 ]] && _isroot=true

###################################################################
## Dotfiles list: 		
## $ ls -d -1 .* |cut -f1 -d'/' |column



################################################################################
## Dir colors (default is /etc/DIR_COLORS) run dircolors to see
if [ -f $HOME/.dir_colors_256 ]; then
	eval $(dircolors -b $HOME/.dir_colors_256)
fi

################################################################################
## Colors and prompts (needs cleanup)
#TERM=xterm-256color 

case "$TERM" in
       xterm*) TERM=xterm-256color
esac


################################################################################
# PS1 Final
if [ $(id -u) -eq 0 ]; then
	PS1='\[\e[1;91m\]\u@\[\e[m\]\[\e[1;91m\]\H\[\e[m\] \[\e[1;96m\]\w\[\e[m\] \[\e[1;31m\]\$\[\e[m\] \[\e[1;37m\]'
else
	PS1='\[\e[1;92m\]\u@\[\e[m\]\[\e[1;92m\]\H\[\e[m\] \[\e[1;96m\]\w\[\e[m\] \[\e[1;32m\]\$\[\e[m\] \[\e[1;37m\]'
fi

unset color_prompt force_color_prompt



################################################################################
# Colors
# Reset
Off='\e[0m'       # Text Reset

# Regular Colors
Black='\e[0;30m'        # Black
Red='\e[0;31m'          # Red
Green='\e[0;32m'        # Green
Yellow='\e[0;33m'       # Yellow
Blue='\e[0;34m'         # Blue
Purple='\e[0;35m'       # Purple
Cyan='\e[0;36m'         # Cyan
White='\e[0;37m'        # White

# Bold
BBlack='\e[1;30m'       # Black
BRed='\e[1;31m'         # Red
BGreen='\e[1;32m'       # Green
BYellow='\e[1;33m'      # Yellow
BBlue='\e[1;34m'        # Blue
BPurple='\e[1;35m'      # Purple
BCyan='\e[1;36m'        # Cyan
BWhite='\e[1;37m'       # White

# Underline
UBlack='\e[4;30m'       # Black
URed='\e[4;31m'         # Red
UGreen='\e[4;32m'       # Green
UYellow='\e[4;33m'      # Yellow
UBlue='\e[4;34m'        # Blue
UPurple='\e[4;35m'      # Purple
UCyan='\e[4;36m'        # Cyan
UWhite='\e[4;37m'       # White

# Background
On_Black='\e[40m'       # Black
On_Red='\e[41m'         # Red
On_Green='\e[42m'       # Green
On_Yellow='\e[43m'      # Yellow
On_Blue='\e[44m'        # Blue
On_Purple='\e[45m'      # Purple
On_Cyan='\e[46m'        # Cyan
On_White='\e[47m'       # White

# High Intensity
IBlack='\e[0;90m'       # Black
IRed='\e[0;91m'         # Red
IGreen='\e[0;92m'       # Green
IYellow='\e[0;93m'      # Yellow
IBlue='\e[0;94m'        # Blue
IPurple='\e[0;95m'      # Purple
ICyan='\e[0;96m'        # Cyan
IWhite='\e[0;97m'       # White

# Bold High Intensity
BIBlack='\e[1;90m'      # Black
BIRed='\e[1;91m'        # Red
BIGreen='\e[1;92m'      # Green
BIYellow='\e[1;93m'     # Yellow
BIBlue='\e[1;94m'       # Blue
BIPurple='\e[1;95m'     # Purple
BICyan='\e[1;96m'       # Cyan
BIWhite='\e[1;97m'      # White

# High Intensity backgrounds
On_IBlack='\e[0;100m'   # Black
On_IRed='\e[0;101m'     # Red
On_IGreen='\e[0;102m'   # Green
On_IYellow='\e[0;103m'  # Yellow
On_IBlue='\e[0;104m'    # Blue
On_IPurple='\e[0;105m'  # Purple
On_ICyan='\e[0;106m'    # Cyan
On_IWhite='\e[0;107m'   # White




################################################################################
# SCRIPTS & PATHS
#Pandoc installer cabal haskell
export PATH=/home/boban/.cabal/bin:$PATH

#My Perl scripts
export gouda="/home/boban/Scripts/gouda.pl"
export PATH=$PATH:$gouda

#My sync doc script
export syncdocs=/home/boban/Scripts/sync2.sh
export PATH=$PATH:$syncdocs

#export bsync=/home/boban/Scripts/bsync.py
#export PATH=$PATH:$bsync

# Zenity test for colorpicker
export color=/home/boban/Scripts/color_dialog.sh
export PATH=$PATH:$color

# Test for not installed packages to run from /usr/local/bin
export PATH=$PATH:/usr/local/bin/SpriterR4_64

# Gem executables: keydown (see https://github.com/infews/keydown )
# See arch wiki: https://wiki.archlinux.org/index.php/Ruby#Bundler
PATH="$(ruby -e 'print Gem.user_dir')/bin:$PATH"

# for install python-virtualenv
export WORKON_HOME=${HOME}/Snakepit
if [ -f /usr/local/bin/virtualenvwrapper.sh ]; then
	source /usr/local/bin/virtualenvwrapper.sh
elif [ -f /usr/bin/virtualenvwrapper.sh ]; then
	source /usr/bin/virtualenvwrapper.sh
fi

################################################################################
## EXPORTS 
export PATH=/usr/local/bin:$PATH
export _JAVA_OPTIONS='-Dswing.defaultlaf=com.sun.java.swing.plaf.gtk.GTKLookAndFeel'

################################################################################
#Ruby support
if which ruby &>/dev/null; then
	GEM_DIR=$(ruby -rubygems -e 'puts Gem.user_dir')/bin
	if [[ -d "$GEM_DIR" ]]; then
	  export PATH=$GEM_DIR:$PATH
	fi
	fi
	if which google-chrome-stable &>/dev/null; then
	export CHROME_BIN=/usr/bin/google-chrome-stable
fi

################################################################################
## MODIFIED COMMANDS 
alias ..='cd ..'
alias ....='cd ../..'
alias df='df -h'
alias diff='colordiff'              # requires colordiff package
alias du='du -c -h'
alias free='free -m'                # show sizes in MB
alias grep='grep --color=auto'
alias grep='grep --color=tty -d skip'
alias mkdir='mkdir -p -v'
alias more='less'
alias nano='nano -w'
alias nnan='nano -w'
alias nnao='nano -w'
alias n='nano -w'
alias ping='ping -c 5'

################################################################################
## LS 
alias ls='ls -hF --color=auto'
alias lr='ls -R'                    # recursive ls
alias ll='ls -alh'
alias la='ll -A'
alias lm='la | more'

# lso in function for adding parameters

lso() {
	ls -alh "$@" --color=auto | awk '{k=0;for(i=0;i<=8;i++)k+=((substr($1,i+2,1)~/[rwx]/)*2^(8-i));if(k)printf(" %0o ",k);print}';
}



################################################################################
# SSH

################################################################################
# APACHE
## apache and mysql start,stop restart
alias on='sudo systemctl start httpd;sudo systemctl start mysqld;'
alias off='sudo systemctl stop httpd;sudo systemctl stop mysqld;'
alias both='sudo systemctl restart httpd;sudo systemctl restart mysqld;'

################################################################################
# FILESYSTEM
## see permissions in numbers
#alias lso="ls -alG | awk '{k=0;for(i=0;i<=8;i++)k+=((substr(\$1,i+2,1)~/[rwx]/)*2^(8-i));if(k)printf(\" %0o \",k);print}'"

##alias misc, requires argument
alias his='history | grep '
##alias folders-files
alias lsdirs="ls -d -1 $PWD/**"
alias lsfiles="ls -d -1 $PWD/*.*"
##current dirsize,sort by size low-high, show total
alias size='sudo du -cha --max-depth=1  | sort -h'

################################################################################
# OTHERS
## calibrate Wacom Cintiq
alias calibrate='xsetwacom --set "8" MaptoOutput 1600x1200+1680+0'
alias virtual2.7='mkvirtualenv -p /usr/bin/python2.7 --no-site-packages'
alias vboxmods='sudo modprobe -a vboxdrv vboxnetadp vboxnetflt'

################################################################################
## BASH OPTIONS 
shopt -s cdspell                 # Correct cd typos
shopt -s checkwinsize            # Update windows size on command
shopt -s histappend              # Append History instead of overwriting file
shopt -s cmdhist                 # Bash attempts to save all lines of a multiple-line command in the same history entry
shopt -s extglob                 # Extended pattern
shopt -s no_empty_cmd_completion # No empty completion

################################################################################
## HISTORY CONTROL BOB  
export HISTCONTROL=ignoredups:erasedups  # no duplicate entries
export HISTSIZE=100000                   # big big history
export HISTFILESIZE=100000               # big big history
export HISTCONTROL=ignoreboth   # ingore duplicates and spaces
export HISTIGNORE='&:ls:ll:la:cd:exit:clear:history'
# shopt -s histappend  # append to history, don't overwrite it(already done see above)
# Save and reload the history after each command finishes
#export PROMPT_COMMAND="history -a;history -c;history -r;$PROMPT_COMMAND"
export PROMPT_COMMAND="${PROMPT_COMMAND:+$PROMPT_COMMAND$'\n'}history -a;history -c;history -r"

################################################################################
## COMPLETION 
complete -cf sudo
if [[ -f /etc/bash_completion ]]; then
  . /etc/bash_completion
fi

################################################################################
## EDITOR 
export EDITOR=nano

################################################################################
# COLORED MANUAL PAGES 
## @see http://www.tuxarena.com/?p=508
## For colourful man pages (CLUG-Wiki style)
if $_isxrunning; then
  export PAGER=less
  export LESS_TERMCAP_mb=$'\E[01;31m'       # begin blinking
  export LESS_TERMCAP_md=$'\E[01;38;5;74m'  # begin bold
  export LESS_TERMCAP_me=$'\E[0m'           # end mode
  export LESS_TERMCAP_se=$'\E[0m'           # end standout-mode
  export LESS_TERMCAP_so=$'\E[38;5;246m'    # begin standout-mode - info box
  export LESS_TERMCAP_ue=$'\E[0m'           # end underline
  export LESS_TERMCAP_us=$'\E[04;38;5;146m' # begin underline
fi

################################################################################
## PACMAN ALIASES archlinux
if $_isarch; then
  # we're not root
  if ! $_isroot; then
	alias pacman='sudo pacman'
  fi
  alias pacupg='pacman -Syu'            # Synchronize with repositories and then upgrade packages that are out of date on the local system.
  alias pacupd='pacman -Sy'             # Refresh of all package lists after updating /etc/pacman.d/mirrorlist
  alias pacin='pacman -S'               # Install specific package(s) from the repositories
  alias pacinu='pacman -U'              # Install specific local package(s)
  alias pacre='pacman -R'               # Remove the specified package(s), retaining its configuration(s) and required dependencies
  alias pacun='pacman -Rcsn'            # Remove the specified package(s), its configuration(s) and unneeded dependencies
  alias pacinfo='pacman -Si'            # Display information about a given package in the repositories
  alias pacse='pacman -Ss'              # Search for package(s) in the repositories

  alias pacupa='pacman -Sy && sudo abs' # Update and refresh the local package and ABS databases against repositories
  alias pacind='pacman -S --asdeps'     # Install given package(s) as dependencies of another package
  alias pacclean="pacman -Sc"           # Delete all not currently installed package files
  alias pacmake="makepkg -fcsi"         # Make package from PKGBUILD file in current directory
fi



################################################################################
## Dotfiles extra TOC
################################################################################
# Github: gclone, gcomm, gpush
# extract
# compress: usage: compress <foo.tar.gz> ./foo ./bar
# to_iso: Converts raw, bin, cue, ccd, img, mdf, nrg cd/dvd image files to ISO image file. Usage: to_iso file1 file2...
# ff: Find a file with a pattern in name
# fe: Find a file with pattern $1 in name and Execute $2 on it
# lowercase: Move filenames to lowercase
# dirsize: Finds directory sizes and lists them for the current directory
# screenrec: ffmpeg screencast recorder (hardcode output.mkv)
# screendec: ffmpeg screencast decoder (hardcode output.mkv)
# function screendec_better (hardcode file): our_final_product.mp4
# youtube-dl: yt_title, yt_uploader
# screenshots: shot, shot2 (maim), shotim (imagmagick)
# netinfo: netinfo about network
# extract_simple : simple extract
# function: aa_mod_parameters
# function: show_mod_parameter_info
# screenfetch system info:
# colors: Color dialog
# dummy: Make dummy images
# ASCII fun: buba, hond, worm, asciiquarium




## FUNCTIONS
################################################################################
# GITHUB

gclone () {
	git clone https://github.com/boban-dj/$1
}

gcomm () {
	git commit -a -m $1
}

gpush () {
	git push origin master
}


################################################################################
## ARCHIVE EXTRACTOR 
extract() {
  clrstart="\033[1;34m"  #color codes
  clrend="\033[0m"

  if [[ "$#" -lt 1 ]]; then
	echo -e "${clrstart}Pass a filename. Optionally a destination folder. You can also append a v for verbose output.${clrend}"
	exit 1 #not enough args
  fi

  if [[ ! -e "$1" ]]; then
	echo -e "${clrstart}File does not exist!${clrend}"
	exit 2 #file not found
  fi

  if [[ -z "$2" ]]; then
	DESTDIR="." #set destdir to current dir
  elif [[ ! -d "$2" ]]; then
	echo -e -n "${clrstart}Destination folder doesn't exist or isnt a directory. Create? (y/n): ${clrend}"
	read response
	#echo -e "\n"
	if [[ $response == y || $response == Y ]]; then
	  mkdir -p "$2"
	  if [ $? -eq 0 ]; then
		DESTDIR="$2"
	  else
		exit 6 #Write perms error
	  fi
	else
	  echo -e "${clrstart}Closing.${clrend}"; exit 3 # n/wrong response
	fi
  else
	DESTDIR="$2"
  fi

  if [[ ! -z "$3" ]]; then
	if [[ "$3" != "v" ]]; then
	  echo -e "${clrstart}Wrong argument $3 !${clrend}"
	  exit 4 #wrong arg 3
	fi
  fi

  filename=`basename "$1"`

  #echo "${filename##*.}" debug

  case "${filename##*.}" in
	tar)
	  echo -e "${clrstart}Extracting $1 to $DESTDIR: (uncompressed tar)${clrend}"
	  tar x${3}f "$1" -C "$DESTDIR"
	  ;;
	gz)
	  echo -e "${clrstart}Extracting $1 to $DESTDIR: (gip compressed tar)${clrend}"
	  tar x${3}fz "$1" -C "$DESTDIR"
	  ;;
	tgz)
	  echo -e "${clrstart}Extracting $1 to $DESTDIR: (gip compressed tar)${clrend}"
	  tar x${3}fz "$1" -C "$DESTDIR"
	  ;;
	xz)
	  echo -e "${clrstart}Extracting  $1 to $DESTDIR: (gip compressed tar)${clrend}"
	  tar x${3}f -J "$1" -C "$DESTDIR"
	  ;;
	bz2)
	  echo -e "${clrstart}Extracting $1 to $DESTDIR: (bzip compressed tar)${clrend}"
	  tar x${3}fj "$1" -C "$DESTDIR"
	  ;;
	zip)
	  echo -e "${clrstart}Extracting $1 to $DESTDIR: (zipp compressed file)${clrend}"
	  unzip "$1" -d "$DESTDIR"
	  ;;
	rar)
	  echo -e "${clrstart}Extracting $1 to $DESTDIR: (rar compressed file)${clrend}"
	  unrar x "$1" "$DESTDIR"
	  ;;
	7z)
	  echo -e  "${clrstart}Extracting $1 to $DESTDIR: (7zip compressed file)${clrend}"
	  7za e "$1" -o"$DESTDIR"
	  ;;
	*)
	  echo -e "${clrstart}Unknown archieve format!"
	  exit 5
	  ;;
  esac
}


################################################################################
## ARCHIVE COMPRESS 
compress() {
	if [[ -n "$1" ]]; then
	FILE=$1
	case $FILE in
	*.tar ) shift && tar cf $FILE $* ;;
	*.tar.bz2 ) shift && tar cjf $FILE $* ;;
	*.tar.gz ) shift && tar czf $FILE $* ;;
	*.tgz ) shift && tar czf $FILE $* ;;
	*.zip ) shift && zip $FILE $* ;;
	*.rar ) shift && rar $FILE $* ;;
	esac
	else
	echo "usage: compress <foo.tar.gz> ./foo ./bar"
	fi
}


################################################################################
## CONVERT TO ISO
to_iso () {
  if [[ $# == 0 || $1 == "--help" || $1 == "-h" ]]; then
	echo -e "Converts raw, bin, cue, ccd, img, mdf, nrg cd/dvd image files to ISO image file.\nUsage: to_iso file1 file2..."
  fi
  for i in $*; do
	if [[ ! -f "$i" ]]; then
	  echo "'$i' is not a valid file; jumping it"
	else
	  echo -n "converting $i..."
	  OUT=`echo $i | cut -d '.' -f 1`
	  case $i in
			*.raw ) bchunk -v $i $OUT.iso;; #raw=bin #*.cue #*.bin
	  *.bin|*.cue ) bin2iso $i $OUT.iso;;
	  *.ccd|*.img ) ccd2iso $i $OUT.iso;; #Clone CD images
			*.mdf ) mdf2iso $i $OUT.iso;; #Alcohol images
			*.nrg ) nrg2iso $i $OUT.iso;; #nero images
				* ) echo "to_iso don't know de extension of '$i'";;
	  esac
	  if [[ $? != 0 ]]; then
		echo -e "${R}ERROR!${W}"
	  else
		echo -e "${G}done!${W}"
	  fi
	fi
  done
}


################################################################################
# FILE & STRINGS RELATED FUNCTIONS 
## Find a file with a pattern in name 
ff () { find . -type f -iname '*'$*'*' -ls ; }

## Find a file with pattern $1 in name and Execute $2 on it 
fe () { find . -type f -iname '*'$1'*' -exec "${2:-file}" {} \;  ; }

## Move filenames to lowercase 
lowercase () {
	for file ; do
	  filename=${file##*/}
	  case "$filename" in
	  */* ) dirname==${file%/*} ;;
		* ) dirname=.;;
	  esac
	  nf=$(echo $filename | tr A-Z a-z)
	  newname="${dirname}/${nf}"
	  if [[ "$nf" != "$filename" ]]; then
		mv "$file" "$newname"
		echo "lowercase: $file --> $newname"
	  else
		echo "lowercase: $file not changed."
	  fi
	done
}



### Finds directory sizes and lists them for the current directory 
dirsize () {
	du -shx * .[a-zA-Z0-9_]* 2> /dev/null | egrep '^ *[0-9.]*[MG]' | sort -n > /tmp/list
	egrep '^ *[0-9.]*M' /tmp/list
	egrep '^ *[0-9.]*G' /tmp/list
	rm -rf /tmp/list
}




################################################################################
## FFMPEG SCREENREC SCREENDEC
alias screenrec='ffmpeg -f alsa -ac 2 -i pulse -f x11grab -r 30 -s 1024x768 -i :0.0 -acodec pcm_s16le -vcodec libx264 -preset ultrafast -crf 0 -threads 0 output.mkv'
alias screendec='ffmpeg -i output.mkv -acodec libvorbis -ab 128k -ac 2 -vcodec libx264 -preset slow -crf 22 -threads 0 our-final-product.mp4'

## FFMPEG SCREENDECODING BETTER CODE?
screendec_better () {
	ffmpeg -i "$1" -acodec libvorbis -ab 128k -ac 2 -vcodec libx264 -preset slow -crf 22 -threads 0 our-final-product.mp4
	echo "successfully converted to file"
}

## YOUTUBE-DL
alias yt_title="youtube-dl --write-description --write-thumbnail -o '%(title)s/%(title)s-%(id)s.%(ext)s'"
alias yt_uploader="youtube-dl --write-description --write-thumbnail -o '%(uploader)s/%(title)s-%(id)s.%(ext)s'"

################################################################################
## SCREENSHOT WITH MAIM AND SLOP 
## <https://github.com/naelstrof/maim>
alias shot2='maim -s -c 1,0,0,0.6 -p 10 ~/Pictures/Screenshot/$(date +%F-%T).png'

## SHOT - TAKES A SCREENSHOT OF YOUR CURRENT WINDOW
shot () {
import -frame -strip -quality 75 "$HOME/Pictures/Screenshot/$(date +%s).png"
}

## SCREENSHOT WITH CONVERT IMAGEMAGICK
alias shotimagick='import -window root my1.png'


################################################################################
## NETINFO - SHOWS NETWORK INFORMATION FOR YOUR SYSTEM
netinfo () {
	echo "--------------- Network Information ---------------"
	/sbin/ifconfig | awk /'inet addr/ {print $2}'
	/sbin/ifconfig | awk /'Bcast/ {print $3}'
	/sbin/ifconfig | awk /'inet addr/ {print $4}'
	/sbin/ifconfig | awk /'HWaddr/ {print $4,$5}'
	myip=`lynx -dump -hiddenlinks=ignore -nolist http://checkip.dyndns.org:8245/ | sed '/^$/d; s/^[ ]*//g; s/[ ]*$//g' `
	echo "${myip}"
	echo "---------------------------------------------------"
}


################################################################################
## EXTRACT - EXTRACT MOST COMMON COMPRESSION TYPES
extract_simple () {
	if [ -f $1 ] ; then
	case $1 in
	*.tar.bz2)   tar xjf $1        ;;
	*.tar.gz)    tar xzf $1     ;;
	*.bz2)       bunzip2 $1       ;;
	*.rar)       rar x $1     ;;
	*.gz)        gunzip $1     ;;
	*.tar)       tar xf $1        ;;
	*.tbz2)      tar xjf $1      ;;
	*.tgz)       tar xzf $1       ;;
	*.zip)       unzip $1     ;;
	*.Z)         uncompress $1  ;;
	*.7z)        7z x $1    ;;
	*)           echo "'$1' cannot be extracted via extract()" ;;
	esac
	else
	echo "'$1' is not a valid file"
	fi
}



################################################################################
## SEE KERNEL MODULES LOADED AND PARAMETERS
function aa_mod_parameters () { 
	N=/dev/null;
	C=`tput op` O=$(echo -en "\n`tput setaf 2`>>> `tput op`");
	for mod in $(cat /proc/modules|cut -d" " -f1);
	do
	md=/sys/module/$mod/parameters;
	[[ ! -d $md ]] && continue;
	m=$mod;
	d=`modinfo -d $m 2>$N | tr "\n" "\t"`;
	echo -en "$O$m$C";
	[[ ${#d} -gt 0 ]] && echo -n " - $d";
	echo;
	for mc in $(cd $md; echo *);
	do
	de=`modinfo -p $mod 2>$N | grep ^$mc 2>$N|sed "s/^$mc=//" 2>$N`;
	echo -en "\t$mc=`cat $md/$mc 2>$N`";
	[[ ${#de} -gt 1 ]] && echo -en " - $de";
	echo;
	done;
	done
}


################################################################################
## MORE KERNEL MODULES INFO WITH PARAMETERS AND COLOR
function show_mod_parameter_info () {
	if tty -s <&1
	then
	green="\e[1;32m"
	yellow="\e[1;33m"
	cyan="\e[1;36m"
	reset="\e[0m"
	else
	green=
	yellow=
	cyan=
	reset=
	fi
	newline="
	"

	while read mod
	do
	md=/sys/module/$mod/parameters
	[[ ! -d $md ]] && continue
	d="$(modinfo -d $mod 2>/dev/null | tr "\n" "\t")"
	echo -en "$green$mod$reset"
	[[ ${#d} -gt 0 ]] && echo -n " - $d"
	echo
	pnames=()
	pdescs=()
	pvals=()
	pdesc=
	add_desc=false
	while IFS="$newline" read p
	do
	if [[ $p =~ ^[[:space:]] ]]
	then
	pdesc+="$newline    $p"
	else
	$add_desc && pdescs+=("$pdesc")
	pname="${p%%:*}"
	pnames+=("$pname")
	pdesc=("    ${p#*:}")
	pvals+=("$(cat $md/$pname 2>/dev/null)")
	fi
	add_desc=true
	done < <(modinfo -p $mod 2>/dev/null)
	$add_desc && pdescs+=("$pdesc")
	for ((i=0; i<${#pnames[@]}; i++))
	do
	printf "  $cyan%s$reset = $yellow%s$reset\n%s\n" \
	${pnames[i]} \
	"${pvals[i]}" \
	"${pdescs[i]}"
	done
	echo

	done < <(cut -d' ' -f1 /proc/modules | sort)
}


################################################################################
# SCREENFETCH this is showing the archlogo with some conky-like info when cli starts
#screenfetch


################################################################################
# Color dialog
colors() {
	local fgc bgc vals seq0

	printf "Color escapes are %s\n" '\e[${value};...;${value}m'
	printf "Values 30..37 are \e[33mforeground colors\e[m\n"
	printf "Values 40..47 are \e[43mbackground colors\e[m\n"
	printf "Value  1 gives a  \e[1mbold-faced look\e[m\n\n"

	# foreground colors
	for fgc in {30..37}; do
		# background colors
		for bgc in {40..47}; do
			fgc=${fgc#37} # white
			bgc=${bgc#40} # black

			vals="${fgc:+$fgc;}${bgc}"
			vals=${vals%%;}

			seq0="${vals:+\e[${vals}m}"
			printf "  %-9s" "${seq0:-(default)}"
			printf " ${seq0}TEXT\e[m"
			printf " \e[${vals:+${vals+$vals;}}1mBOLD\e[m"
		done
		echo; echo
	done
}



# Create dymmy images for some reason
# todo: userinput, size, amount of images
function dummy (){
	mkdir ./images
	cd ./images
	convert -size 300x300  gradient:blue              gradient_range1_300w.jpg
	convert -size 300x300  gradient:yellow            gradient_range2_300w.jpg
	convert -size 300x300  gradient:green-yellow      gradient_range3_300w.jpg
	convert -size 300x300  gradient:red-blue          gradient_range4_300w.jpg
	convert -size 300x300  gradient:tomato-steelblue  gradient_range5_300w.jpg
	convert -size 300x300  gradient:snow-navy          gradient_ice-sea_300w.jpg
	convert -size 300x300  gradient:gold-firebrick     gradient_burnished_300w.jpg
	convert -size 300x300  gradient:yellow-limegreen   gradient_grassland_300w.jpg
	convert -size 300x300  gradient:khaki-tomato       gradient_sunset_300w.jpg
	convert -size 300x300  gradient:darkcyan-snow      gradient_snow_scape_300w.jpg
	echo "10 Dummy images 300x300 created!"
}




################################################################################
# ASCII FUN
## BUBA
alias buba='for((P=10**8,Q=P/100,X=320*Q/(`tput cols`-1),Y=210*Q/`tput lines`,y=-105*Q,v=-220*Q,x=v;y<105*Q;x=v,y+=Y));do for((;x<P;a=b=i=k=c=0,x+=X));do for((;a*a+b*b<2*P*P&&i++<99;a=((c=a)*a-b*b)/P+x,b=2*c*b/P+y));do :;done;(((j=(i<99?i%16:0)+30)>37?k=1,j-=8:0));echo -ne "\E[$k;$j"mE;done;echo -e "\E[0m";done #Charles Cooke'

## WORM
alias worm='echo -ne "\033#8";X=`tput cols`;Y=`tput lines`;((a=$X/2));((b=$Y/2));d=1;while case $d in 0)((a=a<2?X:a-1));;1)((b=b<2?Y:b-1));;2)((a=a==X?1:a+1));;3)((b=b==Y?1:b+1));; esac;do ((c=b+a*X));v=${k[c]:- };[ $v. = @. ]&&{((d=d>2?0:d+1));k[c]="";}||{(( d=d<1?3:d-1));k[c]=@;};echo -ne "\033[$b;${a}H$v";done'

## ASCIIQUARIUM ??
function vis () {
	perl /usr/bin/asciiquarium
}

## HONDJE ZINGEN
alias hond='vlc -I dummy -V caca `youtube-dl -g "https://www.youtube.com/watch?v=_7vkRTylYoA"`'
