#!/home/mitya/testenv/bin/python -B                                                                                   
import os
import sys
from datetime import datetime

import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import *
import numpy.ma as ma
import netcdftime
import time as tm
from calendar import monthrange
import datetime 
from datetime import date, time
import argparse
import z_coord
import vert


parser = argparse.ArgumentParser(description='transect write 0.1')

parser.add_argument(
'-i', 
help='input file', 
dest='inf', 
action="store"
)
parser.add_argument(
'-zeta', 
help='input zeta file', 
dest='zeta', 
action="store"
)
parser.add_argument(
'-o', 
help='output file', 
dest='outf', 
action="store"
)
parser.add_argument(
'-grid', 
help='grid file for output', 
dest='grid', 
action="store",
default="/home/mitya/models/NorROMS/Apps/Common/Grid/arctic4km_grd.nc"
)
parser.add_argument(
'-field', 
help='modification parameters', 
dest='field', 
action="store"
)



args = parser.parse_args()


Ni=75
No=35
#theta_si=6.0; theta_bi=0.1; Tclinei=30
theta_so=6.0; theta_bo=0.1; Tclineo=100
#Vtransformi=2; Vstretchingi=1
Vtransformo=2; Vstretchingo=2

f = Dataset(args.inf)
depth = f.variables["deptht"][:]

try:
    zeta = f.variables["zeta"][:]
except:
    zeta_f = Dataset(args.zeta)
    zeta=zeta_f.variables["zeta"][:]
    zeta_f.close()

try:
    mask_rho=f.variables["mask_rho"][:]
    hi = f.variables["h"][:]
except:
    grid = Dataset(args.grid)
    mask_rho=grid.variables["mask_rho"][:]
    hi = grid.variables["h"][:]
    grid.close()


print "hi", hi.shape


z_ro = z_coord.spec_vert_grid(No,hi,zeta[0,:],Tclineo,theta_bo,theta_so,Vtransformo,Vstretchingo,[zeta[0,:].shape[0],zeta[0,:].shape[1]])

print z_ro.shape
print np.amax(z_ro), np.amin(z_ro)
print "...."
print depth.shape
depth = depth[::-1]


field = f.variables[args.field][0,::-1,:]
print field.shape, "field"

field_tr = np.transpose(field, (1,2,0))
print field_tr.shape, "transpose"
z_ri= np.zeros(field.shape)
print z_ri.shape
z_ri.T[:]=-depth

z_ri_tran= np.transpose(z_ri, (1,2,0))
print z_ri_tran.shape, "z_ri_tran shape"


undef=1.e+37

array_out = vert.vert_int(field_tr,z_ri_tran,z_ro,undef,mask_rho,mask_rho,[mask_rho.shape[1],mask_rho.shape[0],Ni,No])
if args.field in ['NO3','PHYC']:
    #sanitizing
    array_out[ array_out<0 ] = 0
else:
    pass
print array_out.shape
#print array_out
print array_out.shape, "array_out" 



if not args.outf:
    nc = Dataset(args.inf+"_vert_int", 'w', format='NETCDF3_64BIT')
else:
    nc = Dataset(args.outf, 'w', format='NETCDF3_64BIT')


nc.createDimension('s_rho', No)   
nc.createDimension('eta_rho', mask_rho.shape[0])
nc.createDimension('xi_rho',mask_rho.shape[1])
nc.createDimension('clim_time', None) # unlimited axis (can be appended to).

nc.setncattr("title","field "+args.field)
if args.field == "NO3":
    out_field =  nc.createVariable('NO3', np.float64, ('clim_time','s_rho','eta_rho','xi_rho'))
    out_field.long_name = "Mole Concentration of Nitrate in Sea Water" 
    out_field.units = "mmol.m-3" 
    out_field.time = "clim_time" 
    out_field.field = "scalar, series" 
    nc.variables["NO3"][0,:] = np.transpose(array_out, (2,0,1))
elif args.field == "PHYC":
    out_field =  nc.createVariable('phytoplankton', np.float64, ('clim_time','s_rho','eta_rho','xi_rho'))
    out_field.long_name = "Mole Concentration of Phytoplankton expressed as carbon in sea water" 
    out_field.units = "mmol.m-3" 
    out_field.time = "clim_time" 
    out_field.field = "scalar, series"             
    nc.variables["phytoplankton"][0,:] = np.transpose(array_out, (2,0,1))
else:
    pass


nc.close()
f.close()
