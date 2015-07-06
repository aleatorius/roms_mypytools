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
miss = open("missing_in_rst.txt","w")



def unpack(ina):
    if ina.ndim == 0:
        print "is it scalar or 0d array?"
        outa = ina[()]
    else:
        outa = np.zeros(ina.shape)
        outa[:] = ina[:]
    return outa




#f = Dataset('/home/mitya/vilje_rivers.nc')
f = Dataset(args.inf)
g = Dataset(args.rst)


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

inter_time = []
inter_notime = []


for i in g.variables.keys():
    print i, g.variables[i].dimensions
    try:
        print "try statement"
        print f.variables[i].dimensions
#        for j in f.variables[i].ncattrs():
#            print j, ": ", f.variables[i].getncattr(j), f.variables[i].dimensions
#            w.setncattr(j, f.variables[i].getncattr(j))
        #nc.variables[i][:]=f.variables[i]
#        arr = []
        if any("eta" in s for s in g.variables[i].dimensions):
            if any("time" in l for l in g.variables[i].dimensions):
                if any("eta_rho" in l for l in g.variables[i].dimensions):
                    inter_time.append((i,"rho"))
                elif any("eta_psi" in l for l in g.variables[i].dimensions):
                    inter_time.append((i,"psi"))
                elif any("eta_u" in l for l in g.variables[i].dimensions):
                    inter_time.append((i,"u"))
                elif any("eta_v" in l for l in g.variables[i].dimensions):
                    inter_time.append((i,"v"))
                else:
                    pass
            else:
                inter_notime.append(i)
        else:
            pass
    except:
        miss.write(str(i)+" "+str(g.variables[i].dimensions)+" \n")


#for i,j in enumerate(b[1]):
#        print i,j
#        nc.variables[j][:] = b[i]
print inter_time
print inter_notime
#nc.close()

miss.close()
f.close()
g.close()
