#!/home/mitya/testenv/bin/python -B                                                                                   
# -*- coding: utf-8 -*-
## Dmitry Shcherbin, 2015.03.11
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

parser = argparse.ArgumentParser(
description='add rivers, via txt file',
usage=''
)
parser.add_argument(
'-i', 
help='river netcdf file', 
dest ='inf', 
action="store"
)
parser.add_argument(
'-o', 
help='river netcdf file file', 
dest ='outf', 
action="store"
)
parser.add_argument(
'-river', 
help='rivers txt file', 
dest ='river', 
action="store"
)
parser.add_argument(
'-grid', 
help='grid netcdf file', 
dest ='grid', 
action="store",
default='/home/mitya/models/NorROMS/Apps/Common/Grid/arctic4km_grd.nc'
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


grid_file = args.grid
grid = Dataset(grid_file)
mask = unpack(grid.variables['mask_rho'])
grid.close()
def discharge(annual,width, percent):
    ref = date(1970,6,15)
    ref_time = time(0,0,0)
    # center will be placed on 15 of june
    refer= datetime.datetime.combine(ref, ref_time)

    hvol1= annual*percent/(100.*(365-width)*24)
    hvol2 = annual*(100-percent)/(100.*width*24)
    # box function, centered around 15.06, percent outside, (100-percent) of annual discharge inside
    border1 = (refer - datetime.timedelta(width/2.))
    border2 = (refer + datetime.timedelta(width/2.))
    box_range=range(int(border1.strftime("%m")),int(border2.strftime("%m")))
    box_range.append(int(border2.strftime("%m")))
    #a1 duration of increased discharge during first month
    a1 = datetime.datetime.combine(date(1970, box_range[1],1), time(0,0,0))-border1
    #a2 duration of increased discharge during the last month
    a2 = border2-datetime.datetime.combine(date(1970, box_range[-1],1), time(0,0,0))

    out = np.zeros(12)
    for i in range(1,13):
        if i in box_range:
            if i == box_range[0]:
                out[i-1]=(a1.seconds/3600.+a1.days*24)*hvol2+(monthrange(1970,i)[1]*24-(a1.seconds/3600.+a1.days*24))*hvol1
            elif i == box_range[-1]:
                out[i-1]=(a2.seconds/3600.+a2.days*24)*hvol2+(monthrange(1970,i)[1]*24-(a2.seconds/3600.+a2.days*24))*hvol1
            else:
                out[i-1]= monthrange(1970,i)[1]*24*hvol2
        else:
            out[i-1]= monthrange(1970,i)[1]*24*hvol1
    print "before scaling", out
    for i in range(1,13):
        print monthrange(1970,i)[1]
        out[i-1]=out[i-1]*(1000**3)/(monthrange(1970,i)[1]*24*3600)
    print "after scaling", out
    return out


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
        


def add_dummy_river(input_array):
    new_array= []
    for j,i in enumerate(input_array[0]):
        print i.shape, j, input_array[1][j]
        index= np.zeros(len(i.shape))
        index[:]=i.shape[:]
        index[-1]= index[-1]+1
        print index
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


green = open(args.river,"r")
p = Proj(proj='stere', R=6371000.0, lat_0=90, lat_ts=60.0, x_0=4180000.0, y_0=2570000.0, lon_0=58.0)

output_array = extract_arrays(f) 


for line in green.readlines():
    a = line.split()
    print a


    for i,j in enumerate(a[1:-1]):
        print i,j
        a[i+1]=float(j)
        print a[i]
    print a
#    a[2]=a[2]*(1000**3)/(365*24*3600)
    print a[1],a[2]
    a[1],a[2]=np.array(p(a[2],a[1]))/4000.
    print a[1],a[2]
    b = add_dummy_river(output_array)
    for i,j in enumerate(b[1]):
        if j=='river_Xposition':
 #           print i,j
            b[0][i][-1]= int(a[1])
#            print b[1][i],": \n", b[0][i]
            break
    for i,j in enumerate(b[1]):
        if j=='river_Eposition':
#            print i,j
            b[0][i][-1]= int(a[2])
#            print b[1][i],": \n", b[0][i]
            break
    for i,j in enumerate(b[1]):
        if j=='river':
#            print i,j
            b[0][i][-1]=int(b[0][i][-2])+1
#            print b[1][i],": \n", b[0][i]
            break
    for i,j in enumerate(b[1]):
        if j=='river_transport':
#            print i,j
            if a[0]=="a":
                b[0][i][:,-1]=discharge(a[3],a[4],5)
            else:
                b[0][i][:,-1]=a[3:-1]
#            print b[1][i],": \n", b[0][i]
            break
    output_array = b

    

nc = Dataset(args.outf, 'w', format='NETCDF3_CLASSIC')
for i in f.ncattrs():
    print i, f.getncattr(i)
    nc.setncattr(i, f.getncattr(i))
nc.delncattr('history')
nc.setncattr('history', f.getncattr('history')+'\n Modified by '+str(os.path.basename(__file__))+' '+str(tm.strftime("%c")))


#for i in f.dimensions.keys():
#    print i
#    nc.createDimension(i, len(f.dimensions[i]))

for i,j in enumerate(output_array[1]):
    if j=='river':
        print i,j
        nc.createDimension('river', len(output_array[0][i]))        
        break
nc.createDimension('river_time', len(f.dimensions['river_time']))
nc.createDimension('s_rho', len(f.dimensions['s_rho']))



# variables containers and attributes
for i in f.variables.keys():
    print i, f.variables[i].dimensions
    w = nc.createVariable(i, 'f8',  f.variables[i].dimensions)

    for j in f.variables[i].ncattrs():
   #     print j, ": ", f.variables[i].getncattr(j), f.variables[i].dimensions
        w.setncattr(j, f.variables[i].getncattr(j))

# assigning updated values to variables

for i,j in enumerate(output_array[1]):
    print i,j
    nc.variables[j][:] = output_array[0][i]


nc.close()
f.close()
