#!/usr/bin/env python 
##!/home/ntnu/mitya/virt_env/virt1/bin/python -B
## Dmitry Shcherbin, 2014.11.10
import numpy as np
from numpy import *
from netCDF4 import *
import sys, re, glob, os
import numpy.ma as ma
import argparse
import os.path
import datetime
from datetime import date, time
import pprint
from pprint import *
import matplotlib.pyplot as plt
from pylab import *
from matplotlib import colors, cm


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
dest='output', 
action="store", 
default="mass.txt"
)
parser.add_argument(
'-v', 
help='variable', 
dest ='variable', 
action="store"
)
parser.add_argument(
'-f', 
help='time format', 
dest='time_f', 
action="store", 
default="s"
)
parser.add_argument(
'--contourf', 
help='colormesh or contourf', 
dest='contourf',
choices=("yes","no"), 
action="store", 
default="no"
)
parser.add_argument(
'--array', 
help='array or loop', 
dest='array',
choices=("yes","no"), 
action="store", 
default="no"
)
parser.add_argument(
'--res', 
help='resolution, fraction of minimum distance between layers', 
dest='res', 
action="store", 
default=2
)
parser.add_argument(
'--extras', 
help='s-layers', 
dest='extras',
choices=('yes', 'no'), 
action="store", 
default="no"
)
parser.add_argument(
'--graphics', 
help='graphics', 
choices=('yes', 'no'), 
dest='graphics', 
action="store", 
default="yes"
)
parser.add_argument(
'--interpolate', 
help='vertical interpolation, off by default', 
choices=('yes', 'no'), 
dest='interpolate', 
action="store", 
default="no"
)
parser.add_argument(
'--time_rec', 
help='time rec',
dest ='time_rec', 
action="store", 
default="ocean_time"
)
parser.add_argument(
'--time', 
help='time counter', 
dest ='time', 
action="store", 
type=int, 
default=0
)
parser.add_argument(
'--vert', 
help='vertical coordinate number', 
dest ='vert', 
action="store", 
type=int, 
default=34
)
parser.add_argument(
'--xzoom', 
help='zoom along x(?) direction, range is defined in percents', 
dest ='xzoom', 
action="store",  
default='0:100'
)
parser.add_argument(
'--yzoom', 
help='zoom along y(?) direction, range is defined in percents', 
dest ='yzoom', 
action="store",  
default='0:100'
)
parser.add_argument(
'--var_min', 
help='minimum value of variable', 
dest ='var_min', 
action="store", 
type=float, 
default = None
)
parser.add_argument(
'--var_max', 
help='minimum value of variable', 
dest ='var_max', 
action="store", 
type=float, 
default = None
)
args = parser.parse_args()

if not (args.inf):
    parser.error('please give a file name')
if not os.path.isfile(args.inf):
     print 'file does not exists'
     parser.error('please give a file name')
     

if ':' not in list(args.xzoom):
     parser.error('provide zoom in i:k format!')
else:
     for i in [0,1]:
          if 0 <= float(args.xzoom.split(':')[i])<= 100:
               pass
          else:
               parser.error('whole range 0:100')

if ':' not in list(args.yzoom):
     parser.error('provide zoom in i:k format!')
else:
     for i in [0,1]:
          if 0 <= float(args.yzoom.split(':')[i])<= 100:
               pass
          else:
               parser.error('wrong xzoom, whole range 0:100')


if float(args.yzoom.split(':')[0])>= float(args.yzoom.split(':')[1]):
     parser.error('in zoom range i:k i<k')
if float(args.xzoom.split(':')[0])>= float(args.xzoom.split(':')[1]):
     parser.error('in zoom range i:k i<k')

def print_list(data):
    col_width = max(len(i) for i in data) + 2  # padding
    count = 0
    a= []
    for i in data:
        count = count +1
        if count < 6:
            a.append(i)
        else:
            print "".join(j.ljust(col_width) for j in a)
            a = []
            count = 0


def date_time(ot):
     ref = date(1970,01,01)
     ref_time = time(0,0,0)
     refer= datetime.datetime.combine(ref, ref_time)
     if args.time_f =='s':
         return (refer + datetime.timedelta(float(ot)/(3600*24))).strftime("%Y-%m-%d") #%H:%M:%S")
     else:
         return (refer + datetime.timedelta(float(ot))).strftime("%Y-%m-%d")# %H:%M:%S")


if not (args.variable):
    f = Dataset(args.inf)
    print_list(f.variables.keys())
    f.close()
    sys.exit()

def unpack(ina):
    if ina.ndim == 0:
        print "is it scalar or 0d array?"
        outa = ina[()]
    else:
        outa = zeros(ina.shape)
        outa[:] = ina[:]
    return outa

def extract_lat_lon(inf):
    f = Dataset(inf)
    lat = unpack(f.variables["lat_rho"])
    lon = unpack(f.variables["lon_rho"])
    f.close()
    return lat, lon

def extract_vert(inf, inv):
     f = inf
     if str(inv) in f.variables.keys():
#          print '\n In the file', inf
          print 'variable', inv, 'exists'
          ncvar = unpack(f.variables[inv])
          print 'the grid dimensions of requested variable:', ncvar.shape

     else:
          print 'provided variable doesnt exists, choose from the list:\n'
          print_list(f.variables.keys())          
          f.close()
          sys.exit()

     return ncvar


def extract(inf, variable, time, vert):
    f = inf
    if str(variable) in f.variables.keys():
 #       print '\n In the file', inf
        print 'variable', variable, 'exists'
        ncvar = unpack(f.variables[variable][time,:])
        print 'and its dimension equals:', size(ncvar.shape)+1
        if size(ncvar.shape) == 3:
            ncvar = unpack(f.variables[variable][time,vert,:])
        if size(ncvar.shape) == 1:
            print 'possibly there is no time dimension, so it is shown as it is'
            ncvar = unpack(f.variables[variable])
        else:
            pass
        print 'the grid dimensions of requested variable:', ncvar.shape

    else:
        print 'provided variable doesnt exists, choose from the list:\n'
        print_list(f.variables.keys())          
        f.close()
        sys.exit()
    times = (args.time_rec, "time", "clim_time", "bry_time")
    result = False
    for t in times:
        try:
            print t
            ot = unpack(f.variables[str(t)])  
            result = True
            break
        except KeyError:
             #e = sys.exc_info()[0]
            print "key error, trying another name for time record"
            continue
        print result
    if result == False:
        print "there is no time var with names", times
        sys.exit()
    else:
        pass
    return ncvar, ot

def extract_vertical(inf, variable, time):
     f = inf
     if str(variable) in f.variables.keys():
  #        print '\n In the file', inf
          print 'variable', variable, 'exists'
          ncvar = unpack(f.variables[variable][time,:])
     else:
          print 'provided variable doesnt exists, choose from the list:\n'
          print_list(f.variables.keys())          
          f.close()
          sys.exit()
     times = (args.time_rec, "time", "clim_time", "bry_time")
     result = False
     for t in times:
         try:
             print t
             ot = unpack(f.variables[str(t)])  
             result = True
             break
         except KeyError:
             #e = sys.exc_info()[0]
             print "key error, trying another name for time record"
             continue
         print result
     if result == False:
         print "there is no time var with names", times
         sys.exit()
     else:
         pass
     return ncvar, ot


#def z_r(index,zeta,h,s_rho, hc, Cs_r,N):
#    z_r = zeros((int(N)))
#    for k in range(N):
        #print k
        #print h[index]
#        z0 = (hc * s_rho[k] + h[index]*Cs_r[k])/(hc + h[index])
#        z_r[k]  = zeta[index] + (zeta[index] + h[index])*z0
#    return z_r




def z_w_a(zeta,h,s_w, hc, Cs_w,Np, Vtransform):
    z_w = zeros((int(Np),h.shape[0],h.shape[1]))
    if Vtransform == 2 or Vtransform == 4:
        for k in range(Np):
            z0 = (hc * s_w[k]*np.ones(h.shape) + h*Cs_w[k])/(hc + h)
            z_w[k]  = zeta + (zeta + h)*z0
    elif Vtransform == 1:
#not tested
        for k in range(Np):
            z0 = hc * s_w[k]*np.ones(h.shape) + (h - hc*np.ones(h.shape)) * Cs_w[k]
            z_w[k] = z0 + zeta * (np.ones(h.shape) + z0/h)
    return z_w

#extract data from netcdf
f = Dataset(args.inf)
meta =  extract(f, args.variable, args.time, args.vert)
meta_trans = extract_vertical(f, args.variable, args.time)[0]
meta =  extract(f, args.variable, args.time, args.vert)
ze =  extract(f, "zeta", args.time, args.vert)[0]
mask_rho =  extract(f, "mask_rho", args.time, args.vert)[0]
zeta = ma.masked_outside(ze, -1e+36,1e+36)
Cs_r = extract_vert(f, 'Cs_r')
s_rho = extract_vert(f, 's_rho')
Cs_w = extract_vert(f, 'Cs_w')
s_w = extract_vert(f, 's_w')
Vtransform = extract_vert(f, 'Vtransform')
Vstretching = extract_vert(f, 'Vstretching')
N = len(s_rho)
Np = len(s_w)
print Np, "Np", N, "N"
#Tcline = extract_vert(args.inf, 'Tcline')
#theta_s = extract_vert(args.inf, 'theta_s')
#theta_b = extract_vert(args.inf, 'theta_b')
hc= extract_vert(f, 'hc')
#print Vtransform, Vstretching, N,Tcline, hc, theta_s, theta_b
h_m =  extract(f, "h", args.time, args.vert)[0]
h = ma.masked_outside(h_m, -1e+36,1e+36)
f.close()



ncvar = meta[0]
ocean_time = meta[1]
print ocean_time
print date_time(ocean_time[args.time])
#lat, lon = extract_lat_lon(args.inf)
#fillval = 1e+36


#masked data
mx = ma.masked_outside(ncvar, -1e+36,1e+36)
mx_trans = ma.masked_outside(meta_trans, -1e+36,1e+36)





#

mesh_integ=ma.masked_where(mask_rho==0,np.sum(np.diff(z_w_a(zeta, h, s_w,hc, Cs_w,Np,Vtransform), axis=0)*meta_trans, axis=0))

print Vtransform

def hisdate(his):
     ref=date(1970,01,01)
     outdate = (ref + datetime.timedelta(float(int(his))/(3600*24))).strftime("%Y_%m_%d")
     return outdate
fillval=1e+36
#mesh_masked = ma.masked_outside(mesh_integ,-fillval,fillval)
mesh_masked=mesh_integ
outfile=str(args.variable)+"_"+args.output               
if os.path.isfile(outfile):
    print "file does exist at this time"
    out_file = open(outfile, 'a')
else:
    print "no such file, creating one"
    out_file = open(outfile, 'w')

out_file.write(str(date_time(ocean_time[args.time]))+" "+str(np.sum(mesh_masked))+"\n")
out_file.close()



if args.graphics=="yes":
    cmap=plt.cm.spectral
    fig_mesh = plt.figure(figsize=(22,8)) 
    

    ax_z = fig_mesh.add_subplot(121)
    ax_mesh = fig_mesh.add_subplot(122)

 
    if args.contourf=="yes":
        pm=ax_mesh.contourf(mesh_masked, cmap=cmap)
        pz=ax_z.contourf(ma.masked_where(mask_rho==0,z_w_a(zeta, h, s_w,hc, Cs_w,Np,Vtransform)[0]), cmap=cmap)
    else:
        pm=ax_mesh.pcolormesh(mesh_masked, cmap=cmap)
#        pz=ax_z.pcolormesh(mesh_masked, cmap=cmap)
        pz=ax_z.pcolormesh(ma.masked_where(mask_rho==0,np.diff(z_w_a(zeta, h, s_w,hc, Cs_w,Np,Vtransform),axis=0)[34]), cmap=cmap)
    plt.colorbar(pm, cmap=cmap, orientation="vertical")           
    plt.colorbar(pz, cmap=cmap, orientation="horizontal")           
    plt.title(args.variable+' '+ date_time(meta[1][args.time])+'\n '+str(np.sum(mesh_masked)))

    if args.var_min or args.var_max:
        if args.var_min and args.var_max:
            if args.var_min < args.var_max:
                p.set_clim(float(args.var_min), float(args.var_max))
            else:
                print 'incorrect var_min shoud be less than var_max, defaults then'
                pass
        else:
            p.set_clim(args.var_min, args.var_max)
    else:
        pass
    plt.axis('tight')
    plt.show()



else:
    pass


exit
#format axes


                
                

                


