#!/bin/bash

## USAGE
# ./datediff.sh '2013-07-22 11:55:19' '2015-12-25 02:00:13'
#02 years 06 months 04 days 16 hours 04 minutes 54 seconds

#$ ./datediff.sh '2013-07-22 11:55:19' '2013-12-25 02:00:13'
#06 months 05 days 16 hours 04 minutes 54 seconds

firstdate=$1;
secondate=$2;

fullyear=$(date -d@$(( ( $(date -ud "$secondate" +'%s') - $(date -ud "$firstdate" +'%s') ) )) +'%Y years %m months %d days %H hours %M minutes %S seconds')
yearsubtraction=$(( $(echo $fullyear | sed -r 's/^([0-9]+).*/\1/') - 1970 ))

if [ $yearsubtraction -le '0' ]; then
  echo $fullyear | sed -r "s/^([0-9]+) years //" 
else
  echo $fullyear | sed -r "s/^([0-9]+) /$(printf %02d $yearsubtraction) /"
fi
