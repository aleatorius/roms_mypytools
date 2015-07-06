#!/bin/bash


#source /etc/profile.d/modules.sh

set -x
extract='zeta'
datstamp=`date +%Y_%m_%d_%H_%M`
pathout=/global/work/mitya/arctic20_test_jens/
mydir=${PWD#*}


echo $mydir
exec 1>$mydir/split.log 2>&1


for file in "$@"
do
    echo $file
    counter=0
    a=00$((counter+1))
    if [ -f $file ]; then
	echo "file exists"
	echo $file
    else 
	echo "no file" 1>&2
	exit 1
    fi
    dirbase=${file%/*}
    filebase=${file##*/}
    filename=${filebase%.*}
    fileout=$dirbase/${extract}_$filename
    echo $fileout
    while ncks -O -d clim_time,$counter -v $extract $file ${fileout}_$a.nc > /dev/null
    do
	counter=$((counter+1))
	echo $counter
	l=$((counter+1))
	len="${#l}"
	echo $len
	if [ "$len" -eq "1" ]; then
	    a=00$((counter+1))
	else
	    if [ "$len" -eq "2" ]; then
		a=0$((counter+1))
	    else
		a=$((counter+1))
	    fi
	fi
    done
done
set +x
exit

