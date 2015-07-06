#!/bin/bash
#PBS -o /global/work/mitya/metno/FOAM_reanalysis/scripts/prep_o.log
#PBS -j oe
#PBS -N Arctic20km
##PBS -l select=32:ncpus=32:mpiprocs=16:ompthreads=16:mem=29000mb
##PBS -l select=64:ncpus=32:mpiprocs=16:ompthreads=16:mem=29000mb
##PBS -l select=64:ncpus=32:mpiprocs=16:ompthreads=1:mem=29000mb
#PBS -lnodes=2:ppn=2
#PBS -lpmem=2000MB
#PBS -l walltime=00:09:59
#xoPBS -A nn9300k
#PBxoS -V
#PBS -q express

set -x
datstamp=`date +%Y_%m_%d_%H_%M`
exec 1>/global/work/mitya/metno/FOAM_reanalysis/scripts/bio_convert_20km.log_${datstamp} 2>&1

module load intel/13.0  
module load nco netcdf/4.2.1.1 boost/1.52.0 #proj udunits boost hdf5 

#################################################################
fimex_path=/home/mitya/bin/fimex
#roms2roms_path=/home/metno/nilsmk/models/romstools/roms2roms
#roms2roms_path=/work/nilsmk/Forcing/MyOcean/Vert_interp/src/roms2roms
roms2roms_path=/home/mitya/roms2roms_bio/roms2roms

basepath=/global/work/mitya/metno
patho=$basepath/FOAM_reanalysis/ROMS_ready/
rawpath=/global/work/mitya/metno/MyOcean
grdfile=/home/mitya/models/NorROMS/Apps/Common/Grid/arctic20km_grd.nc

cd $basepath/FOAM_reanalysis/scripts

years="2007 2008"
#years="2004 2005"
#months="02"
months="01 02 03 04 05 06 07 08 09 10 11 12"
biotracers="NO3 PHYC"

Ni=75;
No=35;
theta_so=6.0; theta_bo=0.1; Tclineo=30
Vtransformo=2; Vstretchingo=1

#################################################################

# Reference time to be used in ROMS simulation. Default set to
# 1970-01-01 00:00:00
YYr=1970; MMr=01; DDr=01; HHr=00

for yy in $years; do
    for mm in $months; do
	rho_file=$basepath/FOAM_reanalysis/tmp_files/MyOcean_climatology_rho_${yy}${mm}.nc
#	u_file=$basepath/FOAM_reanalysis/tmp_files/MyOcean_climatology_u_${yy}${mm}.nc	
#	v_file=$basepath/FOAM_reanalysis/tmp_files/MyOcean_climatology_v_${yy}${mm}.nc

        # Temperature and sea surface elevation
	rawfile=$rawpath/$yy/MyOcean_file_${yy}${mm}_1
	temp_and_zeta=$basepath/FOAM_reanalysis/tmp_files/MyOcean_climatology_zeta_and_T_${yy}${mm}.nc
        # deflate
	echo "unzip $rawfile" > deflate.sh
	sh deflate.sh > filename.txt
	grep -o *gz filename.txt  > infile.txt
	read inputfile_tmp < infile.txt 
	gzip -d $inputfile_tmp
	len=${#inputfile_tmp}
	pos=`expr $len - 3`
	inputfile=${inputfile_tmp:0:$pos}
	rm deflate.sh filename.txt infile.txt 

	orgcfgfile=$basepath/FOAM_reanalysis/fimex_config_20km/fimex_MyOcean.cfg_ORIG
	newcfgfile=fimex_MyOcean.cfg
	itxt='INPUTFILE'
	cp $orgcfgfile tmp1.fil
	perl -pe "s#$itxt#$inputfile#g" < tmp1.fil > tmp2.fil
	mv tmp2.fil tmp1.fil

	itxt='OUTPUTFILE'
	perl -pe "s#$itxt#$temp_and_zeta#g" < tmp1.fil > tmp2.fil
	mv tmp2.fil tmp1.fil

	mv tmp1.fil $newcfgfile

	echo `pwd`
	echo `ls`

	${fimex_path} -c $newcfgfile -n 16
	ncrename -v votemper,temp -v sossheig,zeta -v lon,lon_rho -v lat,lat_rho $temp_and_zeta
	ncrename -d deptht,depth -v deptht,depth $temp_and_zeta
	ncrename -d time_counter,time -v time_counter,time $temp_and_zeta
	ncatted -O -h -a coordinates,zeta,o,c,"lon_rho lat_rho" $temp_and_zeta
	ncatted -O -h -a coordinates,temp,o,c,"lon_rho lat_rho" $temp_and_zeta
  	python $basepath/python_scripts/edit_time.py $temp_and_zeta $YYr $MMr $DDr $HHr
	rm $inputfile $newcfgfile
 	mv $temp_and_zeta  $rho_file

	for bt in $biotracers; do
	    echo $bt
	    biofile='BIOMER_FREEGLORYS2V3_'$yy$mm'15_R20140410_grid'$bt'.nc'
	    echo $biofile
	    inputfile=$rawpath/$yy/$biofile
	    outputfile=$basepath/FOAM_reanalysis
	    rho_bio=$basepath/FOAM_reanalysis/tmp_files/${bt}_rho_bio_${yy}${mm}.nc
	    orgcfgfile=$basepath/FOAM_reanalysis/fimex_config_20km/fimex_MyOcean.cfg_ORIG
	    newcfgfile=fimex_MyOcean.cfg
	    itxt='INPUTFILE'
	    cp $orgcfgfile tmp1.fil
	    perl -pe "s#$itxt#$inputfile#g" < tmp1.fil > tmp2.fil
	    mv tmp2.fil tmp1.fil

	    itxt='OUTPUTFILE'
	    perl -pe "s#$itxt#$rho_bio#g" < tmp1.fil > tmp2.fil
	    mv tmp2.fil tmp1.fil

	    mv tmp1.fil $newcfgfile

	    echo `pwd`
	    echo `ls`

	    ${fimex_path} -c $newcfgfile -n 16
	    ncrename -d deptht,depth -v deptht,depth -v $bt,input $rho_bio
	    ncrename -d time_counter,time -v time_counter,time $rho_bio

	
  	    python $basepath/python_scripts/edit_time.py $rho_bio $YYr $MMr $DDr $HHr

	    rho_file_bio=$rho_bio
 	    ofile=${bt}_bio_ocean_$yy$mm; igtypr=1;  Vstretchingi=1
	    theta_si=3.0; theta_bi=0.4; Tclinei=10; Vtransformi=0
 	    ${roms2roms_path} <<EOF
$rho_file
$Ni $theta_si $theta_bi $Tclinei
$rho_file
$rho_file_bio
$Vtransformi $Vstretchingi
$grdfile
$No $theta_so $theta_bo $Tclineo
$patho
$ofile
$Vtransformo $Vstretchingo
EOF

	    ncrename -v output,$bt ${patho}${ofile}_clm.nc
#	ncks -A -a -v lon_rho,lat_rho $rho_file	${patho}${ofile}_clm.nc
#	ncks -A -a -v lon_u,lat_u $u_file	${patho}${ofile}_clm.nc
# 	ncks -A -a -v lon_v,lat_v $v_file	${patho}${ofile}_clm.nc
# 	ncatted -O -h -a calendar,clim_time,o,c,"gregorian" ${patho}${ofile}_clm.nc
	rm $rho_bio
	done
    done
done

set +x

exit
