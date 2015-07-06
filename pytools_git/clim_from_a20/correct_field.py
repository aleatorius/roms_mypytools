#!/home/mitya/testenv/bin/python -B                                                                                   
import os
import sys
from datetime import datetime

import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import *
from numpy import *
import netcdftime
import time as tm
from calendar import monthrange
import datetime 
from datetime import date, time
import argparse
parser = argparse.ArgumentParser(description='transect write 0.1')

parser.add_argument(
'-i', 
help='input file', 
dest='inf', 
action="store"
)
parser.add_argument(
'-o', 
help='output file', 
dest='outf', 
action="store"
)
parser.add_argument(
'-field', 
help='modification parameters', 
dest='field', 
action="store"
)



args = parser.parse_args()


def unpack(ina):
    if ina.ndim == 0:
        print "is it scalar or 0d array?"
        outa = ina[()]
    else:
        outa = np.zeros(ina.shape)
        outa[:] = ina[:]
    return outa


#grid_file = '/home/ntnu/mitya/models/NorROMS/Apps/Common/Grid/arctic4km_grd.nc'
#grid = Dataset(grid_file)
#mask = unpack(grid.variables['mask_rho'])
#grid.close()

#f = Dataset('/home/mitya/vilje_rivers.nc')
f = Dataset(args.inf)


def extract_arrays(f):
    var_array = []
    var_name = []
    for i in f.variables.keys():
        print i
        var_name.append(i)
        var_array.append(unpack(f.variables[i]))
    return var_array, var_name
        




#original data
b = extract_arrays(f) 
print b[1]
#sys.exit()

if args.field:
    if not args.outf:
        nc = Dataset(args.inf+"_corrected", 'w', format='NETCDF3_64BIT')
    else:
        nc = Dataset(args.outf, 'w', format='NETCDF3_64BIT')
    for i in f.ncattrs():
        print i, f.getncattr(i)
        nc.setncattr(i, f.getncattr(i))
    nc.delncattr('history')
    nc.setncattr('history', f.getncattr('history')+'\n Modified by '+str(os.path.basename(__file__))+' '+str(tm.strftime("%c")))


    for i in f.dimensions.keys():
        print i
        nc.createDimension(i, len(f.dimensions[i]))

    for i in f.variables.keys():
        print i, f.variables[i].dimensions
        w = nc.createVariable(i, 'f8',  f.variables[i].dimensions)

        for j in f.variables[i].ncattrs():
       #     print j, ": ", f.variables[i].getncattr(j), f.variables[i].dimensions
            w.setncattr(j, f.variables[i].getncattr(j))

    # assigning updated values to variables

    for i,j in enumerate(b[1]):
        print i,j
        if j=="hice":
            print "hice exists"
            c = b[0][i][:]
            print c.shape
            c[ c<0 ] = 0
            print np.amin(c),np.amax(c)
            nc.variables[j][:] = c
        elif j=="aice":
            print "aice exists"
            c = b[0][i][:]
            print c.shape
            c[ c<0 ] = 0
            c[ c>1 ] = 1
            print np.amin(c),np.amax(c)
            nc.variables[j][:] = c
        elif j=="ti":
            print "ti exists"
            c = b[0][i][:]
            print c.shape
            c[ c>0 ] = 0
            print np.amin(c),np.amax(c)
            nc.variables[j][:] = c
        elif j=="snow_thick":
            print "snow_thick exists"
            c = b[0][i][:]
            print c.shape
            c[ c<0 ] = 0
            print np.amin(c),np.amax(c)
            nc.variables[j][:] = c
        elif j=="temp":
            print "temp exists"
            c = b[0][i][:]
            print c.shape
            c[ c>1000 ] = 1e+37
            print np.amin(c),np.amax(c)
            nc.variables[j][:] = c
        elif j=="sfwat":
            print "sfwat exists"
            c = b[0][i][:]
            print c.shape
            c[ c<0 ] = 0
            print np.amin(c),np.amax(c)
            nc.variables[j][:] = c
        else:
            nc.variables[j][:] = b[0][i]

    nc.close()

else:
    pass

f.close()
