#!/bin/bash
##mitya shcherbin' modification of yoshie script
#PBS -o /global/work/mitya/yoshie/prep_o.log
##put your paths!
#PBS -j oe
#PBS -N yoshie_data_2003_2010
#PBS -lnodes=1:ppn=1
#PBS -lpmem=29000MB
#PBS -l walltime=00:59:59
#PBS -A nn9300k
##project number!
#PBS -V
##PBS -q express
#-----------------------------------------------
#-----------------------------------------------

set -x

datstamp=`date +%Y_%m_%d_%H_%M`
WORK=/work/mitya
pathRun=${WORK}
exec 1>$pathRun/log_${datstamp} 2>&1

stations="34,372 50,400 22,334"

module load netcdf 

cd $pathRun


for st in $stations; do
    IFS=',' read -ra single <<< "$st"
    echo ${single[0]},${single[1]}
    python ~/pytools_git/time_series_monthly.py -station ${single[0]} ${single[1]}
done



set +x
exit
