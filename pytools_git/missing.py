#!/home/mitya/testenv/bin/python -B                                            # -*- coding: utf-8 -*-                                     
import os
import sys
from datetime import datetime

import numpy as np
from netCDF4 import Dataset

import netcdftime
import time as tm
from calendar import monthrange
import datetime 
from datetime import date, time
import argparse
# load boost before: module load boost/1.53.0 nco

parser = argparse.ArgumentParser(description='transect write 0.1')

parser.add_argument(
'-rst', 
help='input sample rst file', 
dest='rst', 
action="store"
)
parser.add_argument(
'-i', 
help='input file', 
dest='inf', 
action="store"
)
parser.add_argument(
'-o', 
help='input file', 
dest='outf', 
action="store"
)



args = parser.parse_args()
miss = open("missing_in_rst.txt","r")



def unpack(ina):
    if ina.ndim == 0:
        print "is it scalar or 0d array?"
        outa = ina[()]
    else:
        outa = np.zeros(ina.shape)
        outa[:] = ina[:]
    return outa




#f = Dataset('/home/mitya/vilje_rivers.nc')


#if not args.outf:
#    nc = Dataset(args.inf+"_filtered", 'w', format='NETCDF3_CLASSIC')
#else:
#    nc = Dataset(args.outf, 'w', format='NETCDF3_CLASSIC')
#for i in f.ncattrs():
#    print i, f.getncattr(i)
#    nc.setncattr(i, f.getncattr(i))
#nc.delncattr('history')
#nc.setncattr('history', f.getncattr('history')+'\n Modified by '+str(os.path.basename(__file__))+' '+str(tm.strftime("%c")))


#for i in f.dimensions.keys():
#    print i
#    nc.createDimension(i, len(f.dimensions[i]))

for i in miss.readlines():
    var = i.split()[0]
    string1="ncks -v "+str(var)+" "+args.rst+" -o inp_"+str(var)+".nc"
    string2= "ncks -A inp_"+str(var)+".nc " + args.inf
    print string1
    print string2
    os.system(string1)
    os.system(string2)
miss.close()

#to merge into one file
#mitya@service0:/work/mitya/interp_a20_a4> mv iniout_zeta.nc output.nc 
#mitya@service0:/work/mitya/interp_a20_a4> f=output.nc 
#mitya@service0:/work/mitya/interp_a20_a4> for i in iniout_*; do ncks -A $i $f;done    
