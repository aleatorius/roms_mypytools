#!/bin/bash
#mitya shcherbin  modification of yoshie script

drc_in='/global/work/apn/Arctic-4km_results/1993_2010_jens/'


#module load nco
fileout=outlist
if [ -f $fileout ]; then
    rm -f $fileout
else
    for file in  `ls ${drc_in}ocean_avg*.nc`; do
	echo $file
	python /home/mitya/bin/ncdate_full $file >> $fileout
    done
fi


