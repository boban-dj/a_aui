#!/bin/bash

# It uses a config file called backup_files, see example
# The backup directory, BK is also created automatically
# then it takes the saved dir "BK" and makes a tar file
# with hostname and date

# example 'backup_files' file:
#
#/home/boban/.bashrc
#/home/boban/Desktop
#/srv/http
#/etc/ssh
#/etc/httpd
#/etc/php
#/etc/mysql
#/etc/iptables


# It is run as follows:
#
#   ~/Scripts/copy_config.sh



# added pacman package listing for easy install with: 
# # xargs -a Packages pacman -S --noconfirm --needed

pacman -Qqe | grep -vx "$(pacman -Qqm)" > /home/boban/Packages
$ pacman -Qqm > /home/boban/Packages.aur

# reading the file backup_files

if [[ $1 == "-l" ]]
then
for i in $(cat ./backup_files)
do
echo $i
done
exit
fi

if [[ $1 == "-h" ]]
then
echo "cb (Config Backup) version 0.1a"
echo "Usage: cb -[lhr]"
echo "-l    Don't copy anything, just display the config file"
echo "-h    Show this help/version"
echo "-r   Restore files"
echo "Written in 2009 by Lexion on Arch Linux"
exit
fi

if [[ $1 == "-r" ]]
then
echo "Putting configs in your home directory,"
echo "you should find them there"
cp -r ./BK/* .
exit
fi

if [ -a ./backup_files ]
then
echo "Starting cb backup process..."
echo "-----------------------------"
else
touch ./backup_files
fi

if [ -d ./BK ]
then
echo "Backing up my own config file..."
cp -r ./backup_files ./BK/backup_files
else
mkdir -p ./BK
fi

for i in $(cat ./backup_files)
do
echo "Backing up" $i"..."
sudo cp -r $i ./BK
done

echo "----------------"
echo "Done backing up."



## make tar from backup files in BK

backup_files=./BK

# Destination of Backup.
dest="."

# Create archive filename.
day=$(date +%Y-%m-%d)
hostname=$(hostname -s)
archive_file="$hostname-$day.tar.gz"

# Print start status message.
echo "Backing up $backup_files to $dest/$archive_file"
date
echo

# Backup The Files using tar.
tar -zcvf $dest/$archive_file $backup_files

# Print end status message.
echo
echo "Backup finished"
date

# Long listing of files in $dest to check file sizes.
ls -lh $dest

