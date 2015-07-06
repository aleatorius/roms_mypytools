#!/home/mitya/testenv/bin/python -B                                                                                   
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



def unpack(ina):
    if ina.ndim == 0:
        print "is it scalar or 0d array?"
        outa = ina[()]
    else:
        outa = np.zeros(ina.shape)
        outa[:] = ina[:]
    return outa



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
    return out

distr = discharge(1000, 130, 5)
print distr, np.sum(distr)
time_units = 'days since 1970-01-01 00:00:00'
utime = netcdftime.utime(time_units)

#f = Dataset('/home/mitya/vilje_rivers.nc')
f = Dataset('/home/mitya/models/NorROMS/Apps/Common/Include/arctic4km_rivers.nc')
#river_Eposition = unpack(f.variables['river_Eposition'])
#river_Xposition = unpack(f.variables['river_Xposition'])
#river_transport = unpack(f.variables['river_transport'])
#river = unpack(f.variables['river'])
#river_direction = unpack(f.variables['river_direction'])
#river_Vshape = unpack(f.variables['river_Vshape'])
#river_salt = unpack(f.variables['river_salt'])
#river_temp = unpack(f.variables['river_temp'])
#river_flag = unpack(f.variables['river_flag'])
#river_time = unpack(f.variables['river_time'])
#print river_e.shape, river_transport.shape, river_temp.shape, river_salt.shape
#print river_flag
#a = np.zeros((12,35))
#print type(a), a.shape
#print type(river_temp), river_temp.shape

#c = np.ones((river_temp.shape[0],river_temp.shape[1],river_temp.shape[2]+1))

#print c.shape, a.shape
#print c[:,:,:-1].shape


#print c
#nc_attrs = f.ncattrs()
var_array = []
var_name = []
def extract_arrays(f):

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




#for i,j in enumerate(b):
#    print a[1][i]
#    print j

#b[0][-1]= 58
#print b[0]

new_rivers = []
green = open("greenland.txt","r")
p = Proj(proj='stere', R=6371000.0, lat_0=90, lat_ts=60.0, x_0=4180000.0, y_0=2570000.0, lon_0=58.0)

output_array = extract_arrays(f) 

for line in green.readlines():
    a = line.split()
    for i,j in enumerate(a[:-1]):
        a[i]=float(j)
    a[2]=a[2]*(1000**3)/(365*24*3600)
    a[0],a[1]=np.array(p(a[1],a[0]))/4000.
    b = add_dummy_river(output_array)
    for i,j in enumerate(b[1]):
        if j=='river_Xposition':
            print i,j
            b[0][i][-1]= int(a[0])
            print b[1][i],": \n", b[0][i]
            break
    for i,j in enumerate(b[1]):
        if j=='river_Eposition':
            print i,j
            b[0][i][-1]= int(a[1])
            print b[1][i],": \n", b[0][i]
            break
    for i,j in enumerate(b[1]):
        if j=='river':
            print i,j
            b[0][i][-1]=int(b[0][i][-2])+1
            print b[1][i],": \n", b[0][i]
            break
    for i,j in enumerate(b[1]):
        if j=='river_transport':
            print i,j
            print b[0][i][:,-1].shape, discharge(a[2],a[3],5).shape
            b[0][i][:,-1]=discharge(a[2],a[3],5)
            print b[1][i],": \n", b[0][i]
            break
    output_array = b

    
#    new_rivers.append(a)
    
    

print new_rivers    

nc = Dataset('edited_rivers.nc', 'w', format='NETCDF3_CLASSIC')
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

print f.variables['river_transport'].ncattrs()
#for i in f.variables['river_transport'].ncattrs():
 #   print i,": ", f.variables['river_transport'].getncattr(i)

for i in f.variables.keys():
    print i, f.variables[i].dimensions
    w = nc.createVariable(i, 'f8',  f.variables[i].dimensions)

    for j in f.variables[i].ncattrs():
   #     print j, ": ", f.variables[i].getncattr(j), f.variables[i].dimensions
        w.setncattr(j, f.variables[i].getncattr(j))


for i,j in enumerate(output_array[1]):
    print i,j
    nc.variables[j][:] = output_array[0][i]


#print river_num, river_transport.shape

#river = river_e

#river_Xposition = river_x

#river_Eposition = river_e


#river_Vshape = vshape
#print river_Vshape.shape, "river_vshape"
###################################
# Crate netCDF file

# dimensions:
#   xi_rho = 575 ;
#   eta_rho = 191 ;
#   s_rho = 30 ;
#   river = 10 ;
#   river_time = 3652 ;
# variables:
#   double river(river) ;
#   double river_Xposition(river) ;
#   double river_Eposition(river) ;
#   double river_direction(river) ;
#   double river_Vshape(s_rho, river) ;
#   double river_time(river_time) ;
#   double river_transport(river_time, river) ;
#   double river_temp(river_time, s_rho, river) ;
#   double river_salt(river_time, s_rho, river) ;
#   double river_flag(river) ;
#   double river_O2(river_time, s_rho, river) ;
#   double river_Miss(river_time, s_rho, river) ;
#   double river_Atch(river_time, s_rho, river) ;
# 
# // global attributes:
#       :title = "TGLO river forcing file" ;
#       :type = "FORCING file" ;
#       :author = "Robert Hetland" ;
#       :date = "20-Nov-2003 18:35:37" ;
# }



#nc.createDimension('x_rho', 671)
#nc.createDimension('eta_rho', 191)


def write_nc_var(name, dimensions, var, units=None, long_name = None):
    nc.createVariable(name, 'f8', dimensions)
    if units is not None:
        nc.variables[name].units = units
    if long_name is not None:
        nc.variables[name].long_name = long_name
    nc.variables[name][:] = var




#write_nc_var('river', ('river', ), river, 'River index')
#write_nc_var('river_Xposition', ('river', ), river_Xposition, 'River xi index')
#write_nc_var('river_Eposition', ('river', ), river_Eposition, 'River eta index')
#write_nc_var('river_direction', ('river', ), river_direction, 'River direction')
#write_nc_var('river_flag', ('river', ), river_flag, 'River flag')

#write_nc_var('river_Vshape', ('s_rho', 'river'), river_Vshape, 'River vertical shape')
#write_nc_var('river_time', ('river_time', ), river_time, time_units)
#write_nc_var('river_transport', ('river_time', 'river'), river_transport, 
#             'River transport [m3/s]', "river runoff vertically integrated mass transport")
#write_nc_var('river_temp', ('river_time', 's_rho', 'river'), 
#              river_temp,
#             'River temperature [deg C]')
#write_nc_var('river_salt', ('river_time', 's_rho', 'river'), river_salt,
#             'River salinity [psu]')

# Tracers
#write_nc_var('river_dye_01', ('river_time', 's_rho', 'river'), river_dye_01,
#            'River oxygen [mmol/l]')
#write_nc_var('river_dye_02', ('river_time', 's_rho', 'river'), river_dye_02,
#            'Mississippi river tag [none]')
#write_nc_var('river_dye_03', ('river_time', 's_rho', 'river'), river_dye_03,
#            'Atchafalaya river tag [none]')
#write_nc_var('river_dye_04', ('river_time', 's_rho', 'river'), river_dye_04,
#            'Brazos river tag [none]')

#write_nc_var('river_Miss', ('river_time', 's_rho', 'river'), river_Miss,
#            'Mississippi river tag [none]')
#write_nc_var('river_Atch', ('river_time', 's_rho', 'river'), river_Atch,
#            'Atchafalaya river tag [none]')

nc.close()
f.close()
