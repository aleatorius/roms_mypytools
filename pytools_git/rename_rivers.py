#!/home/mitya/testenv/bin/python -B                                                                                   
# -*- coding: utf-8 -*-
## Dmitry Shcherbin, 2015.03.16
##!/usr/bin/env python 
import os
import sys
from datetime import datetime
import pyproj
from pyproj import Proj
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

__author__='Dmitry Shcherbin'
__email__='dmitry.shcherbin@gmail.com'


def unpack(ina):
    if ina.ndim == 0:
        print "is it scalar or 0d array?"
        outa = ina[()]
    else:
        outa = np.zeros(ina.shape)
        outa[:] = ina[:]
    return outa


def extract_arrays(f):
    var_array = []
    var_name = []
    for i in f.variables.keys():
        print i
        var_name.append(i)
        var_array.append(unpack(f.variables[i]))
    return var_array, var_name
        



grid_files = ('/home/mitya/models/NorROMS/Apps/Common/Grid/arctic4km_grd.nc','/home/mitya/models/NorROMS/Apps/Common/Grid/arctic20km_grd.nc')
#river_files = ('/home/mitya/models/NorROMS/Apps/Common/Include/arctic4km_rivers.nc', '/home/mitya/models/NorROMS/Apps/Common/Origfiles/A20_rivers_openBering35.nc')
#river_files = ('/home/mitya/vilje_rivers.nc', '/home/mitya/models/NorROMS/Apps/Common/Origfiles/A20_rivers_openBering35.nc')
river_files = ('/home/mitya/pytools_git/a4_rivers.nc', '/home/mitya/pytools_git/a20_rivers.nc')



a20, a4 = Dataset(river_files[1]), Dataset(river_files[0])

a20_array = extract_arrays(a20) 
a4_array = extract_arrays(a4) 

river_record=[]
for i,j in enumerate(a4_array[1]):
    print i,j, a4_array[0][i].shape
    if j=='river':
        river_record.append(i)
    else:  
        pass

for i,j in enumerate(a20_array[1]):
    print i,j, a20_array[0][i].shape
    if j=='river':
        river_record.append(i)
    else:
        pass
    

a20_output_array= a20_array
a4_output_array= a4_array

for rec_num, record in enumerate(a4_array[0][river_record[0]]):
    print record, rec_num
    a4_output_array[0][river_record[0]][rec_num]=rec_num+1

for rec_num, record in enumerate(a20_array[0][river_record[1]]):
    print record, rec_num
    a20_output_array[0][river_record[1]][rec_num]=rec_num+1
    

nc = Dataset('a20_test.nc', 'w', format='NETCDF3_CLASSIC')
for i in a20.ncattrs():
    print i, a20.getncattr(i)
    nc.setncattr(i, a20.getncattr(i))
nc.delncattr('history')
nc.setncattr('history', a20.getncattr('history')+'\n Modified by '+str(os.path.basename(__file__))+' '+str(tm.strftime("%c")))



for i in a20.dimensions.keys():
    print i
    nc.createDimension(i, len(a20.dimensions[i]))


# variables containers and attributes
for i in a20.variables.keys():
    print i, a20.variables[i].dimensions
    w = nc.createVariable(i, 'f8',  a20.variables[i].dimensions)

    for j in a20.variables[i].ncattrs():
   #     print j, ": ", f.variables[i].getncattr(j), f.variables[i].dimensions
        w.setncattr(j, a20.variables[i].getncattr(j))

# assigning updated values to variables




for i,j in enumerate(a20_array[1]):
    print i,j
    nc.variables[j][:] = a20_output_array[0][i]


nc.close()


nc = Dataset('a4_test.nc', 'w', format='NETCDF3_CLASSIC')
for i in a4.ncattrs():
    print i, a4.getncattr(i)
    nc.setncattr(i, a4.getncattr(i))
nc.delncattr('history')
nc.setncattr('history', a4.getncattr('history')+'\n Modified by '+str(os.path.basename(__file__))+' '+str(tm.strftime("%c")))



for i in a4.dimensions.keys():
    print i
    nc.createDimension(i, len(a4.dimensions[i]))


# variables containers and attributes
for i in a4.variables.keys():
    print i, a4.variables[i].dimensions
    w = nc.createVariable(i, 'f8',  a4.variables[i].dimensions)

    for j in a4.variables[i].ncattrs():
   #     print j, ": ", f.variables[i].getncattr(j), f.variables[i].dimensions
        w.setncattr(j, a4.variables[i].getncattr(j))

# assigning updated values to variables




for i,j in enumerate(a4_array[1]):
    print i,j
    nc.variables[j][:] = a4_output_array[0][i]


nc.close()


a20.close()
a4.close()
