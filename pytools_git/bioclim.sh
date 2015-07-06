#!/bin/bash


source /etc/profile.d/modules.sh

set -x
extract='zeta'
datstamp=`date +%Y_%m_%d_%H_%M`
pathclim=/global/work/mitya/Clim/
pathmyocean=/global/work/mitya/temp/
mydir=${PWD#*}

years="2000 2001 2002"
months="01 02 03 04 05 06 07 08 09 10 11 12"
biocomp="NO3 PHYC"

for year in $years; do
    for month in $months; do
	echo $year $month
	echo ${pathclim}zeta_*${year}_clm_0${month}.nc
	echo ${pathmyocean}*GLORYS*${year}${month}*.nc_inter
	for bio in $biocomp; do
	    echo ${pathmyocean}*GLORYS*${year}${month}*${bio}.nc_inter
	    python ~/pytools_git/clim_vertical_transform.py -i ${pathmyocean}*GLORYS*${year}${month}*${bio}.nc_inter -field $bio -zeta ${pathclim}zeta_*${year}_clm_0${month}.nc
	done
	
    done
done
set +x
exit

