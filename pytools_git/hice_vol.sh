#!/bin/bash
set -x
datstamp=`date +%Y_%m_%d_%H_%M`
CWD=$(pwd)
#exec 1>frames.log_${datstamp} 2>&1
##module load netcdf python nco
data=/global/work/jsk/K160
#cd $pathRun
echo $1 $2  ' -> echo $1 $2'
#echo $k
#echo $j
#echo {$k..$j}


years="2007 2008 2009 2010"
for year in $years; do
    files=${data}/norfjords_160m_avg.nc_${year}*
    for i in $files; do
	echo $i
	if foo="$(python /home/mitya/pytools_git/polygon_zoom_2d.py -i $i --pin /home/yoshie/pytools_git/kong_0 -o kong -v hice)"; then 
	    echo "python works"
	else 
	    echo "Could not python! Aborting." 1>&2
	    exit 1
	fi




    done

done
set +x
exit

