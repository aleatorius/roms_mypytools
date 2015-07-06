#!/bin/bash
set -x
datstamp=`date +%Y_%m_%d_%H_%M`
exec 1>/global/work/mitya/rerun_mix/frames.log_${datstamp} 2>&1
##module load netcdf python nco
pathRun=/global/work/mitya/rerun_mix
cd $pathRun
echo $1 $2  ' -> echo $1 $2'
#echo $k
#echo $j
#echo {$k..$j}

for l in $(eval echo {$1..$2});
do
    echo $l
    len="${#l}"
    echo $len
    if [ "$len" -eq "1" ]; then
	a=000$l
    else
	if [ "$len" -eq "2" ]; then
	    a=00$l
	else
	    if [ "$len" -eq "3" ]; then
		a=0$l
	    else
		echo "argument is too long for this dumb script"
	    fi
	fi
    fi
    echo $a
    file=ocean_avg_mix_$a*.nc
    if [ -f $file ]; then
	echo "file exists"
	echo $file
#	if foo="$(/home/mitya/testenv/bin/python -B pymframesperfile.py -o hice -v hice --var_min 0.0 --var_max 8.0 -i $file)"; then 
	if foo="$(python ~/pytools_git/pymframesperfile.py -o flux_a4 -v ssflux --var_min -0.00002 --var_max 0.00005 -i $file --title='a4 mix')"; then 
	    echo "python works"
	    if foo="$(python ~/pytools_git/pymframesperfile.py -o flux_a4 -v shflux --var_min -800 --var_max 200 -i $file --title='a4 mix')"; then 
		echo "it works too"
	    fi
#	    read -a array <<< $foo
#	    echo ${array[0]}, ${array[1]} #
#	    if scp $file mitya@stallo.uit.no:/global/work/mitya/AR_cor2/ocean_his_${array[1]}.nc; then
#		rm $file
#	    else#
#		echo "cannot ssh-copy file"
#		exit 1
#	    fi
	else 
	    echo "Could not python! Aborting." 1>&2
	    exit 1
	fi
    else
	echo "file does not exist"
    fi
done

#/home/mitya/testenv/bin/python -B pymframes.py -o vvel -v v -s 0065 --var_min -2.28693962097 --var_max 3.55173802
set +x
exit
