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
        


def add_dummy_river(input_array):
    new_array= []
    for j,i in enumerate(input_array[0]):
#        print i.shape, j, input_array[1][j]
        index= np.zeros(len(i.shape))
        index[:]=i.shape[:]
        index[-1]= index[-1]+1
        #print index
        arr = np.ones(index)
        if len(index)==1:
            if input_array[1][j]=="river_time":
                index= np.zeros(len(i.shape))
                arr = np.ones(index)
                arr = i 
            else:
                arr[:-1]=i
                arr[-1]=arr[-2]
        elif len(index)==2:
            arr[:,:-1]=i
            arr[:,-1]=arr[:,-2]
        elif len(index)==3:
            arr[:,:,:-1]=i
            arr[:,:,-1]=arr[:,:,-2]
        else:
            print "what is the shape of this array??", index
        new_array.append(arr)
    return new_array, input_array[1]

grid_files = ('/home/mitya/models/NorROMS/Apps/Common/Grid/arctic4km_grd.nc','/home/mitya/models/NorROMS/Apps/Common/Grid/arctic20km_grd.nc')
#river_files = ('/home/mitya/models/NorROMS/Apps/Common/Include/arctic4km_rivers.nc', '/home/mitya/models/NorROMS/Apps/Common/Origfiles/A20_rivers_openBering35.nc')
#river_files = ('/home/mitya/vilje_rivers.nc', '/home/mitya/models/NorROMS/Apps/Common/Origfiles/A20_rivers_openBering35.nc')
river_files = ('/home/mitya/pytools_git/a4_rivers.nc', '/home/mitya/models/NorROMS/Apps/Common/Origfiles/A20_rivers_openBering35.nc')



p = Proj(proj='stere', R=6371000.0, lat_0=90, lat_ts=60.0, x_0=4180000.0, y_0=2570000.0, lon_0=58.0)
a20, a4 = Dataset(river_files[1]), Dataset(river_files[0])

a20_array = extract_arrays(a20) 
a4_array = extract_arrays(a4) 

start_river=58
river_record=[]
riverxpos_record=[]
riverepos_record=[]
transport_record = []
direction_record = []
for i,j in enumerate(a4_array[1]):
    print i,j, a4_array[0][i].shape
    if j=='river':
        river_record.append(i)
        for m,n in enumerate(a4_array[0][i]):
            print m,n
            if int(n)==int(start_river):
                print m,n
                river_record.append(m)
                break
            else:
                pass
    else:  
        pass
    if j=='river_Eposition':
        riverepos_record.append(i)
    else:
        pass
    if j=='river_transport':
        transport_record.append(i)
    else:
        pass
    if j=='river_direction':
        direction_record.append(i)
    else:
        pass
    if j=='river_Xposition':
        riverxpos_record.append(i)
    else:
        pass
    

for i,j in enumerate(a20_array[1]):
    print i,j, a20_array[0][i].shape
    if j=='river':
        river_record.append(i)
        for m,n in enumerate(a20_array[0][i]):
            print m,n
            if int(n)==int(start_river):
                print m,n
                river_record.append(m)
                break
            else:
                pass
    else:  
        pass
    if j=='river_Eposition':
        riverepos_record.append(i)
    else:
        pass
    if j=='river_transport':
        transport_record.append(i)
    else:
        pass
    if j=='river_Xposition':
        riverxpos_record.append(i)
    else:
        pass
    if j=='river_direction':
        direction_record.append(i)
    else:
        pass
    

output_array= a20_array
print output_array[0][0].shape, 'before'
for rec_num, record in enumerate(a4_array[0][river_record[0]][river_record[1]:]):
    print record, rec_num
    output_array = add_dummy_river(output_array)
    output_array[0][river_record[2]][-1]=int(output_array[0][river_record[0]][-2])+1
    output_array[0][riverxpos_record[1]][-1]= a4_array[0][riverxpos_record[0]][river_record[1]+rec_num]    
    output_array[0][riverepos_record[1]][-1] = a4_array[0][riverepos_record[0]][river_record[1]+rec_num]
    output_array[0][riverxpos_record[1]][-1], output_array[0][riverepos_record[1]][-1] =  np.around(np.array(p(p(output_array[0][riverxpos_record[1]][-1]*4000., output_array[0][riverepos_record[1]][-1]*4000., inverse=True)[0],p(output_array[0][riverxpos_record[1]][-1]*4000., output_array[0][riverepos_record[1]][-1]*4000., inverse=True)[1]))/20000.)
    output_array[0][transport_record[1]][:,-1] = a4_array[0][transport_record[0]][:,river_record[1]+rec_num]
    output_array[0][direction_record[1]][-1]= a4_array[0][direction_record[0]][river_record[1]+rec_num]    
    

nc = Dataset('a20_test.nc', 'w', format='NETCDF3_CLASSIC')
for i in a20.ncattrs():
    print i, a20.getncattr(i)
    nc.setncattr(i, a20.getncattr(i))
nc.delncattr('history')
nc.setncattr('history', a20.getncattr('history')+'\n Modified by '+str(os.path.basename(__file__))+' '+str(tm.strftime("%c")))


for i,j in enumerate(a20_array[1]):
    if j=='river':
        print i,j
        nc.createDimension('river', output_array[0][0].shape[0])        
        break
nc.createDimension('river_time', len(a20.dimensions['river_time']))
nc.createDimension('s_rho', len(a20.dimensions['s_rho']))



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
    nc.variables[j][:] = output_array[0][i]


nc.close()
a20.close()
a4.close()
