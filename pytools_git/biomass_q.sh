#!/bin/bash
#PBS -o /global/work/mitya/prep_o.log
#PBS -j oe
#PBS -N biomass
#PBS -lpmem=29000MB
#PBS -l walltime=00:59:59
#PBS -A nn9300k
#PBS -V
##PBS -q express
set -x
datstamp=`date +%Y_%m_%d_%H_%M`
work_dir=/global/work/mitya/run/Arctic-20km/archive_2005_rename
cd $work_dir
exec 1>q_frames.log_${datstamp} 2>&1
##module load netcdf python nco
#pathRun=/global/work/mitya/1993_2010_jens
#cd $pathRun
#echo $1 $2  ' -> echo $1 $2'

#echo $k
bio_var="NO3 detritus phytoplankton zooplankton"
#echo $j
#echo {$k..$j}
k=101
j=108
for l in $(eval echo {$k..$j});
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
    file=ocean_avg_$a*.nc
    if [ -f $file ]; then
	echo "file exists"
	echo $file
	for bio in $bio_var;
	do 
	    if foo="$(python pyint_op.py -v $bio --graphics no -i $file -o massq.txt)"; then 
		echo "python works"
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
	done
    else
	echo "file does not exist"
    fi
done

#/home/mitya/testenv/bin/python -B pymframes.py -o vvel -v v -s 0065 --var_min -2.28693962097 --var_max 3.55173802
set +x
exit