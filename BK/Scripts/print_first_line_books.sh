#!/bin/bash


# source: <http://unix.stackexchange.com/questions/175656/print-first-and-last-line-of-all-files-in-folder>
# bash loops <http://ryanstutorials.net/bash-scripting-tutorial/bash-loops.php>
# print first and list line from *.md

src_dir_gouda=/home/boban/Sites/master-unix/docs

find "$src_dir_gouda" -mindepth 1 -maxdepth 1 -type d -name 'book*'|
while read D;
	do cd $D;
	for file in *.md
	do
		#echo "file: $file"
		#echo -n "first line: "
		cat "$file" | sed -n '/^\s*$/!{p;q}'
		#   echo -n "last line: "
		#   tac "$file" | sed -n '/^\s*$/!{p;q}'
	done;
done


