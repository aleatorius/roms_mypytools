#!/bin/bash
##mitya shcherbin' modification of yoshie script
#PBS -o /global/work/yoshie/prep_o.log
##put your paths!
#PBS -j oe
#PBS -N yoshie_data_2003_2010
#PBS -lnodes=1:ppn=1
#PBS -lpmem=29000MB
#PBS -l walltime=00:10:59
#PBS -A uit-polar-002
##project number!
#PBS -V
#PBS -q express
#-----------------------------------------------
#-----------------------------------------------

set -x

datstamp=`date +%Y_%m_%d_%H_%M`
WORK=/global/work/yoshie
pathRun=${WORK}
exec 1>$pathRun/log_${datstamp} 2>&1

stations="34,372 54,317 63,298 77,304 80,237 112,243 94,241 128,194 58,172 70,171 75,170 80,169 86,168 45,43"

module load netcdf 

cd $pathRun


for st in $stations; do
    IFS=',' read -ra single <<< "$st"
    echo ${single[0]},${single[1]}
    python /home/yoshie/time_series_monthly.py -station ${single[0]} ${single[1]}
done



set +x
exit
