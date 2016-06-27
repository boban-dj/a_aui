#!/bin/bash


## First try

#mydir=/home/user/Sites/docs/

#for f in "$mydir" find book_*/
#do
#	$gouda
#done

#for file in */ .*/ ; do echo "$file is a directory"; done





## Second try


## improved version with rsync bidirectional
$bsync "-p 4000" /home/boban/Sites/master-unix boyacr1q@boya-creations.nl:/home/boyacr1q/public_html/master-unix


cd /home/boban/Sites/master-unix/docs/book_aantekeningen/
$gouda
cd /home/boban/Sites/master-unix/docs/book_apache/
$gouda
cd /home/boban/Sites/master-unix/docs/book_archlinux/
$gouda
cd /home/boban/Sites/master-unix/docs/book_archlinux_install/
$gouda
cd /home/boban/Sites/master-unix/docs/book_atelier/
$gouda
cd /home/boban/Sites/master-unix/docs/book_backups_sync/
$gouda
cd /home/boban/Sites/master-unix/docs/book_cnc/
$gouda
cd /home/boban/Sites/master-unix/docs/book_dotfiles/
$gouda
cd /home/boban/Sites/master-unix/docs/book_drupal/
$gouda
cd /home/boban/Sites/master-unix/docs/book_ffmpeg/
$gouda
cd /home/boban/Sites/master-unix/docs/book_history/
$gouda
cd /home/boban/Sites/master-unix/docs/book_homeserver/
$gouda
cd /home/boban/Sites/master-unix/docs/book_imagemagick/
$gouda
cd /home/boban/Sites/master-unix/docs/book_linuxfun/
$gouda
cd /home/boban/Sites/master-unix/docs/book_macosx/
$gouda
cd /home/boban/Sites/master-unix/docs/book_macosx_his/
$gouda
cd /home/boban/Sites/master-unix/docs/book_my_script_tools/
$gouda
cd /home/boban/Sites/master-unix/docs/book_mysql/
$gouda
cd /home/boban/Sites/master-unix/docs/book_pandoc_gouda/
$gouda
cd /home/boban/Sites/master-unix/docs/book_perl/
$gouda
cd /home/boban/Sites/master-unix/docs/book_php/
$gouda
cd /home/boban/Sites/master-unix/docs/book_python/
$gouda
cd /home/boban/Sites/master-unix/docs/book_study_all/
$gouda
cd /home/boban/Sites/master-unix/docs/book_ubuntu/
$gouda
cd /home/boban/Sites/master-unix/docs/book_ubuntu_installs/
$gouda
cd /home/boban/Sites/master-unix/docs/book_wget_youtube-dl/
$gouda
cd /home/boban/Sites/master-unix/docs/book_windows7/
$gouda




## now upload to server first version with just scp ssh upload, no rsync
#cd home/boban/Sites/master-unix/docs/
#scp -P 4000 -r home/boban/Sites/master-unix/docs/ boyacr1q@boya-creations.nl:/home/boyacr1q/public_html/master-unix/


## improved version with rsync bidirectional
$bsync "-p 4000" /home/boban/Sites/master-unix boyacr1q@boya-creations.nl:/home/boyacr1q/public_html/master-unix
