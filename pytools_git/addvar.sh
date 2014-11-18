#!/bin/bash
set -x
WORK=/global/work/mitya
pathRun=${WORK}/run/Arctic-20km
filein=ocean_ini_nils.nc
nobioin=ocean_ini_nils_bio.nc
if [ -f $nobioin ]; then
    cp -f $filein $nobioin
else
    cp $filein $nobioin
fi

OLDIFS=$IFS
IFS=','
for i in zooplankton,1.0 detritus,1.0 ; do
    set $i
    echo $1 and $2
    ncap -O -h -s "$1=(salt*0.+$2)" ${pathRun}/$nobioin -o ${pathRun}/$nobioin 
done
IFS=$OLDIFS
#
	
#done
mv ${pathRun}/$nobioin ${pathRun}/ocean_ini_nils_withbio.nc

set +x
exit

