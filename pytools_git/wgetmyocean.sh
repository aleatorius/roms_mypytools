#!/bin/bash

#years="1993 1994 1995 1996 1997 1998 1999 2000 2001 2002 2003 2004 2005 2006 2007 2008 2009 2010" 
years="2002" 
# 1994 1995 1996 1997 1998 1999 2000 2001 2002 2003 2004 2005 2006 2007 2008 2009 2010'

months="01 02 03 04 05 06 07 08 09 10 11 12" 
#months="01" 
bio="no3 phyc"
#months="01" 
for yy in $years; do
    for mm in $months; do
	
	for b in $bio;do

	    filein='ftp://ftp.myocean.mercator-ocean.fr/Core/GLOBAL_REANALYSIS_BIO_001_018/dataset-global-nahindcast-bio-001-018-V5-'${b}'/BIOMER_FREEGLORYS2V3_'$yy$mm'15_R20140410_grid'${b^^}'.nc'
	    echo $filein
	    dir=/global/work/mitya/metno/MyOcean/$yy
	    if [ ! -d "$dir" ]; then
		mkdir $dir
	    fi
	    echo $dir
	    cd $dir
	    fileout=$dir/BIOMER_FREEGLORYS2V3_$yy$mm${b^^}.nc
	    echo $fileout
	    wget --ftp-user= --ftp-password='' $filein $fileout
	done

    done
done