#!/home/mitya/testenv/bin/python -B                                                                                   
import os
import sys
from datetime import datetime, date, time
import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
#import netcdftime
import time as tm
#from calendar import monthrange
#import datetime 
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
'-o', 
help='output file', 
dest='outf', 
action="store"
)
parser.add_argument(
'-field', 
help='modification parameters', 
dest='field', 
action="store",
nargs="*"
)



args = parser.parse_args()


#print z_coord.__doc__
#print vert.__doc__
#print vert.vert_int.__doc__
#print z_coord.spec_vert_grid.__doc__

#signatures
#vert_int - Function signature:
#  array_out = vert_int(array_in,z_ri,z_ro,undef,maski,masko,[mp,lp,ni,no])
#Required arguments:
#  array_in : input rank-3 array('f') with bounds (lp,mp,ni)
#  z_ri : input rank-3 array('f') with bounds (lp,mp,ni)
#  z_ro : input rank-3 array('f') with bounds (lp,mp,no)
#  undef : input float
#  maski : input rank-2 array('i') with bounds (lp,mp)
#  masko : input rank-2 array('i') with bounds (lp,mp)
#Optional arguments:
#  mp := shape(array_in,1) input int
#  lp := shape(array_in,0) input int
#  ni := shape(array_in,2) input int
#  no := shape(z_ro,2) input int
#Return objects:
#  array_out : rank-3 array('f') with bounds (lp,mp,no)
#spec_vert_grid - Function signature:
#  z_r = spec_vert_grid(n,h,zt_avg1,tcline,theta_b,theta_s,vtransform,vstretching,[lp,mp])
#Required arguments:
#
#  n : input int
#  h : input rank-2 array('f') with bounds (lp,mp)
#  zt_avg1 : input rank-2 array('f') with bounds (lp,mp)
#  tcline : input float
#  theta_b : input float
#  theta_s : input float
#  vtransform : input int
#  vstretching : input int
#Optional arguments:
#  lp := shape(h,0) input int
#  mp := shape(h,1) input int
#Return objects:
#  z_r : rank-3 array('f') with bounds (lp,mp,n)


#bath20= Dataset("/home/ntnu/mitya/models/NorROMS/Apps/Common/Grid/arctic4km_grd_bath20.nc")






#def unpack(ina):
#    if ina.ndim == 0:
#        print "is it scalar or 0d array?"
#        outa = ina[()]
#    else:
#        outa = np.zeros(ina.shape)
#        outa[:] = ina[:]
#    return outa






def extract_arrays(f):
    var_array = []
    var_name = []
    for i in f.variables.keys():
        print i
        var_name.append(i)
        var_array.append(f.variables[i][:])
    return var_array, var_name
        

bath4 = Dataset("/home/mitya/pytools_git/clim_from_a20/grid4.nc")
f = Dataset(args.inf)


Ni=35
No=35
theta_si=6.0; theta_bi=0.1; Tclinei=30
theta_so=6.0; theta_bo=0.1; Tclineo=100
Vtransformi=2; Vstretchingi=1
Vtransformo=2; Vstretchingo=2



#original data
b = extract_arrays(f) 
#print b[1], b[1].index("zeta")
ho=bath4.variables["h"][:]
print ho.shape, np.amin(ho),np.amax(ho), "ho"
#sys.exit()

#hi = bath4.variables["h"][:]
hi = ho
mask_rho = bath4.variables["mask_rho"][:]
mask_u = bath4.variables["mask_u"][:]
mask_v = bath4.variables["mask_v"][:]
print "hi", hi.shape

print args.inf
print f
zi = b[0][b[1].index("zeta")][:]
print "zi", zi.shape, np.amin(zi),np.amax(zi)

print b[0][b[1].index("zeta")][0,:].shape[0], b[0][b[1].index("zeta")][0,:].shape[1]
#print b[0][b[1].index("clim_time")]

for record,date in enumerate(b[0][b[1].index("ocean_time")]):
    print record, date, np.amax(b[0][b[1].index("zeta")][record,:])
    
    z_ri = z_coord.spec_vert_grid(Ni,hi,b[0][b[1].index("zeta")][record,:],Tclinei,theta_bi,theta_si,Vtransformi,Vstretchingi,[b[0][b[1].index("zeta")][record,:].shape[0],b[0][b[1].index("zeta")][record,:].shape[1]])[:]
    print z_ri.shape
    print np.amax(z_ri), np.amin(z_ri)
    
    z_ro = z_coord.spec_vert_grid(No,ho,b[0][b[1].index("zeta")][record,:],Tclineo,theta_bo,theta_so,Vtransformo,Vstretchingo,[b[0][b[1].index("zeta")][record,:].shape[0],b[0][b[1].index("zeta")][record,:].shape[1]])[:]
    print z_ro.shape
    print np.amax(z_ro), np.amin(z_ro)


    for field in args.field:
        print b[0][b[1].index(field)].shape, "filed ",field 


#inp_tr = np.transpose(b[0][b[1].index(args.field)][0,:], (1,2,0))
#print inp_tr.shape, "transpose"
#print inp_tr[10,200,:]
#print b[0][b[1].index(args.field)][0,:,10,200]

    undef=1.e+37
        
    for field in args.field:
        print field
        if field == "u":
            b[0][b[1].index(field)][record,:] = np.transpose(vert.vert_int(np.transpose(b[0][b[1].index(field)][record,:], (1,2,0)),z_ri[:,:mask_u.shape[1]],z_ro[:,:mask_u.shape[1]],undef,mask_u,mask_u,[mask_u.shape[1],mask_u.shape[0],Ni,No]),(2,0,1))[:]
        elif field == "v":
            b[0][b[1].index(field)][record,:]  =np.transpose( vert.vert_int(np.transpose(b[0][b[1].index(field)][record,:], (1,2,0)),z_ri[:mask_v.shape[0],:],z_ro[:mask_v.shape[0],:],undef,mask_v,mask_v,[mask_v.shape[1],mask_v.shape[0],Ni,No]),(2,0,1))[:]
        else:
            b[0][b[1].index(field)][record,:] = np.transpose(vert.vert_int(np.transpose(b[0][b[1].index(field)][record,:], (1,2,0)),z_ri,z_ro,undef,mask_rho,mask_rho,[b[0][b[1].index("zeta")][0,:].shape[1],b[0][b[1].index("zeta")][0,:].shape[0],Ni,No]), (2,0,1))[:]    
        
#    except:
#        print "not a mask_rho?"
#        sys.exit()



if args.field:
    if not args.outf:
        nc = Dataset(args.inf+"_vert", 'w', format='NETCDF3_64BIT')
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
#        if j==args.field:
#            nc.variables[j][:] = np.transpose(array_out, (2,0,1))
#        else:
#        b[0][i][ b[0][i] > 1.e+30 ] = 1.e+37
        nc.variables[j][:] = b[0][i]

    nc.close()

else:
    pass

f.close()
bath4.close()

