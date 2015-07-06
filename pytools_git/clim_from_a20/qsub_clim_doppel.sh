#!/bin/bash
#PBS -o /global/work/mitya/prep_o.log
#PBS -j oe
#PBS -N biomass
#PBS -lpmem=29000MB
#PBS -l walltime=10:24:59
#PBS -A nn9300k
#PBS -V
#PBS -q express
set -x
datstamp=`date +%Y_%m_%d_%H_%M`
exec 1>/home/mitya/pytools_git/clim_from_a20/frames.log_${datstamp} 2>&1
module load netcdf python nco boost 
pathRun=/global/work/mitya/clim_from_a20_doppel
archive=/global/work/apn/a20LTR/
cd $pathRun
k=307
j=329
#echo $1 $2  ' -> echo $1 $2'
echo $k
echo $j
#echo {$k..$j}

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
		echo "argument is too long"
	    fi
	fi
    fi
    echo $a
    filein=ocean_avg_$a*.nc
    file=$archive$filein
    echo $file
    if [ -f $file ]; then
	output=${pathRun}/a20_clim_${a}.nc
	echo "file exists"
	echo $file

	if foo="$(python /home/mitya/pytools_git/clim_from_a20/clim_clim.py -i $file -clim /global/work/apn/Arctic-4km_results/climatology_1993_2010_4km/ocean_2001_2002_clm.nc -o $output)";then
	    echo "slicing performed"
	else
	    echo "chould not slice, aborting"
	    exit 1
	fi
	if foo="$(python /home/mitya/pytools_git/clim_from_a20/clim_vert.py -i $output -field temp salt u v -o ${output}_inter)"; then
	    echo "vertical transformation"
	else
	    echo "cannot vertically transform"
	    exit 1
	fi  

	if foo="$(ncrename -d ocean_time,clim_time -v ocean_time,clim_time $output)"; then
	    echo "renaming"
	else
	    echo "cannot rename"
	    exit 1
	fi
	if foo="$(python /home/mitya/pytools_git/clim_from_a20/clim_hinter.py -i $output -o $output)"; then
	    echo "horizontal transformation"
	else
	    echo "cannot horizontally transform"
	    exit 1
	fi  
	if foo="$(ncap2 -O -s 'clim_time=double(double(clim_time)/86400)' $output $output)"; then
	    echo "renaming"
	else
	    echo "cannot ncap2"
	    exit 1
	fi
	if foo="$(ncatted -O -a units,clim_time,o,c,"days since 1970-01-01 00:00:00" $output)"; then
	    echo "renaming"
	else
	    echo "cannot ncatted"
	    exit 1
	fi
	if foo="$(ncatted -a time,,m,c,"clim_time" $output)"; then
	    echo "renaming"
	else
	    echo "cannot ncatted"
	    exit 1
	fi

    fi
done


set +x
exit
