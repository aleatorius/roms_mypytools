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
parser = argparse.ArgumentParser(description='transect write 0.1')

parser.add_argument('-i', help='input file', dest='inf', action="store")
parser.add_argument('-is', help='segments vertices', dest='segments', action="store", default="segments")
parser.add_argument('-v', help='variable', dest ='variable', action="store")
parser.add_argument('-f', help='time format', dest='time_f', action="store", default="s")
parser.add_argument('--contourf', help='colormesh or contourf', dest='contourf',choices=("yes","no"), action="store", default="no")
parser.add_argument('--npinter', help='numpy interpolation', dest='npinter',choices=("yes","no"), action="store", default="yes")
parser.add_argument('--res', help='resolution, fraction of minimum distance between layers', dest='res', action="store", type=float, default=2)
parser.add_argument('--extras', help='s-layers', dest='extras',choices=('yes', 'no'), action="store", default="no")
parser.add_argument('--interpolate', help='vertical interpolation, off by default', choices=('yes', 'no'), dest='interpolate', action="store", default="no")
parser.add_argument('--time_rec', help='time rec', dest ='time_rec', action="store", default="ocean_time")
parser.add_argument('--time', help='time counter', dest ='time', action="store", type=int, default=0)
parser.add_argument('--vert', help='vertical coordinate number', dest ='vert', action="store", type=int, default=0)
parser.add_argument('--xzoom', help='zoom along x(?) direction, range is defined in percents', dest ='xzoom', action="store",  default='0:100')
parser.add_argument('--yzoom', help='zoom along y(?) direction, range is defined in percents', dest ='yzoom', action="store",  default='0:100')
parser.add_argument('--var_min', help='minimum value of variable', dest ='var_min', action="store", type=float, default = None)
parser.add_argument('--var_max', help='minimum value of variable', dest ='var_max', action="store", type=float, default = None)
parser.add_argument('--depth_min', help='min depth, positive value', dest ='depth_min', action="store", type=float, default = None)
parser.add_argument('--depth_max', help='max depth, positive value', dest ='depth_max', action="store", type=float, default = None)
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
         return (refer + datetime.timedelta(float(ot)/(3600*24))).strftime("%Y-%m-%d %H:%M:%S")
     else:
         return (refer + datetime.timedelta(float(ot))).strftime("%Y-%m-%d %H:%M:%S")


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
    f = inf
    lat = unpack(f.variables["lat_rho"])
    lon = unpack(f.variables["lon_rho"])
    return lat, lon

def extract_vert(inf, inv):
     f = inf
     if str(inv) in f.variables.keys():
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
     try:
         ot = unpack(f.variables[[s for s in f.dimensions.keys() if "time" in s][0]])
     except:
         print "no time var?"
         ot = []
     return ncvar, ot

def extract_vertical(inf, variable, time):
     f = inf
     if str(variable) in f.variables.keys():
         #print '\n In the file', inf
         print 'variable', variable, 'exists'
         ncvar = unpack(f.variables[variable][time,:])
         # print 'and its dimension equals:', size(ncvar.shape)+1
         # if size(ncvar.shape) == 3:
         #      ncvar = unpack(f.variables[variable][time,vert,:])
         # if size(ncvar.shape) == 1:
         #      print 'possibly there is no time dimension, so it is shown as it is'
         #      ncvar = unpack(f.variables[variable])
         # else:
         #      pass
         # print 'the grid dimensions of requested variable:', ncvar.shape

     else:
         print 'provided variable doesnt exists, choose from the list:\n'
         print_list(f.variables.keys())          
         f.close()
         sys.exit()
     try:
         ot = unpack(f.variables[[s for s in f.dimensions.keys() if "time" in s][0]])
     except:
         print "no time var?"
         ot = []
     return ncvar, ot
# Bresenham's line algorithm (somebody' python implementation from the web)
def get_line(x1, y1, x2, y2):
    points = []
    issteep = abs(y2-y1) > abs(x2-x1)
    if issteep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
    rev = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        rev = True
    deltax = x2 - x1
    deltay = abs(y2-y1)
    error = int(deltax / 2)
    y = y1
    ystep = None
    if y1 < y2:
        ystep = 1
    else:
        ystep = -1
    for x in range(x1, x2 + 1):
        if issteep:
            points.append((y, x))
        else:
            points.append((x, y))
        error -= deltay
        if error < 0:
            y += ystep
            error += deltax
    # Reverse the list if the coordinates were reversed
    if rev:
        points.reverse()
    return points

#taken from here: Trond Kristiansen https://github.com/trondkr/romstools/tree/master/VolumeFlux


#extract data from netcdf
f= Dataset(args.inf)

meta = extract(f, args.variable, args.time, args.vert)
meta_trans = extract_vertical(f, args.variable, args.time)[0]

depth_conts =  f.variables["deptht"][:]
print depth_conts.shape
depth = np.zeros((depth_conts.shape[0],meta[0].shape[-2],meta[0].shape[-1]))
print depth.shape, meta[0].shape
depth.T[:]=depth_conts
#print depth
f.close()

f = Dataset("/home/mitya/models/NorROMS/Apps/Common/Grid/arctic4km_grd.nc")
mask_rho =  extract(f, "mask_rho", args.time, args.vert)[0]
lat, lon = extract_lat_lon(f)
f.close()

ncvar = meta[0]
fillval = 1e+36
import matplotlib.pyplot as plt
from pylab import *
from matplotlib import colors, cm

#masked data
mx = ma.masked_outside(ncvar, -1e+36,1e+36)
mx_trans = ma.masked_outside(meta_trans, -1e+36,1e+36)
print "mx_trans", mx_trans.shape
cmap=plt.cm.spectral

#event handler

file = open(args.segments,"r")
column,lat_vert,lon_vert,vert,absx,lx,ly =[],[],[],[],[],[],[]
dy= []
z_dict = {}
zr_dict= {}
h_dict = {}
var_dict = {}
#for i in range(Np):
#    z_dict[str(i)]=[]
#for i in range(Np-1):
#    var_dict[str(i)]=[]
#    zr_dict[str(i)]=[]
line_points=[]
counter= 0
xs,ys=[],[]
for line in file:
    i =line.replace("(","").replace(")","").replace(","," ")
    print i.split()
    xs.append(int(i.split()[0]))
    ys.append(int(i.split()[1]))
file.close()
    
if len(xs) > 1:

    for i in range(0,len(xs)-1):
        points=get_line(int(round(xs[i])), int(round(ys[i])), int(round(xs[i+1])),int(round(ys[i+1])))
        #One segment                    
        for j in points:
            if len(line_points)> 0 and line_points[-1]==j:
                pass
            else:
                line_points.append(j)
                counter=counter+1
                lx.append(j[0])
                ly.append(j[1])                    
                dz=[]
                z_dict[str(len(line_points)-1)]= -depth[:,j[1],j[0]]
                var_dict[str(len(line_points)-1)] = mx_trans[:,j[1],j[0]]
         #       zr_dict[str(len(line_points)-1)] =z_r((j[1],j[0]),zeta, h, s_rho,hc, Cs_r,N,Vtransform)
#                print np.diff(z_dict[str(len(line_points)-1)])
#                print min(-(np.diff(z_dict[str(len(line_points)-1)])))
                             
                dy.append(min(-np.diff(z_dict[str(len(line_points)-1)])))
                #print dy
 #               column.append(z_w((j[1],j[0]),zeta, h, s_w,hc, Cs_w,Np, Vtransform)[Np-1]+h[j[1],j[0]])
                lat_vert.append(lat[j[1],j[0]])
                lon_vert.append(lon[j[1],j[0]])
                
                if len(lx) ==1:
                    absx.append(lx[0])
                else:
                    absx.append(absx[-1]+int(sqrt((lx[-1]-lx[-2])**2+(ly[-1]-ly[-2])**2)))


                    #After segment
        if len(vert)==0:
            vert.append((absx[0],lat_vert[0],lon_vert[0],0))
            vert.append((absx[-1],lat_vert[-1],lon_vert[-1],counter))
        else:
            vert.append((absx[-1],lat_vert[-1],lon_vert[-1],counter))
else:
    print  "just one point!"
    exit()

                #all segments are defined, Define mesh
res=args.res
dy = np.asarray(dy)
#dy = dy[~numpy.isnan(dy)]
res=args.res
if len(dy)>0:
    print 
    yincr= min(dy)/res
    print yincr
                #dep =int(round(res*abs(max(column))/min(dy)))                                                                                                                                                   
#    column = np.asarray(z_dict)
    #print column
#    column = column[~numpy.isnan(column)]
    max_depth = abs(np.min(-depth))
    min_depth = abs(np.max(-depth))
    print max_depth, min_depth, ",axmin depth"
    if args.depth_max !=None:
        if max_depth > args.depth_max:
            max_depth = args.depth_max
        else:
            pass
    else:
        pass
    if args.depth_min != None:
        if args.depth_min < max_depth:
            min_depth = args.depth_min
        else:
            pass
    else:
        pass
    dep =int(abs(max_depth-min_depth)/yincr)
    print "resolution", dep
    
else:
    yincr=0.1
    dep=100

#creating mesh - linear interpolaton vertically
mesh_np = np.zeros((dep+10,counter+2))
mesh_np[:]=1e-37

if args.npinter=="yes":
    fnoutcollector=[]
    snoutcollector=[]
    for i in range(len(line_points)):


        if mask_rho[ly[i],lx[i]]==1:
            counter=0
            xp = z_dict[str(i)][::-1]
            print xp
            
            yp = var_dict[str(i)][::-1]
#            yp_nonan = np.asarray(yp)
#            yp_nonan = yp[~yp.mask]
#            print yp_nonan.shape, yp.shape
            depth_max = abs(z_dict[str(i)][-1])
            depth_min = abs(z_dict[str(i)][0])
            fn = "in"
            sn = "in"
            print depth_max, depth_min, fn
            if (args.depth_min != None)  or (args.depth_max != None):
                if (args.depth_min != None) and (args.depth_max!= None):
                    if args.depth_min > args.depth_max:
                        print "wrong range"
                        exit
                    else:
                        if args.depth_min > depth_max:
                            fn = "out"
                            fnoutcollector.append("out")
                        else:
                            depth_min = args.depth_min
                        
                        if args.depth_max > depth_max:
                            pass
                        else:
                            depth_max = args.depth_max
                else:         
                    if args.depth_min != None:
                        if args.depth_min > depth_max:
                            sn = "out"
                            snoutcollector.append("out")
                        else:
                            depth_min = args.depth_min
                    else:
                        pass
                
                    if args.depth_max != None: 
                        if args.depth_max > depth_max:
                            pass
                        else:
                            depth_max = args.depth_max
                    else:
                        pass
            else:
                pass
            print "depths", depth_max, depth_min, fn
            if fn == "out" or sn == "out":
                pass
            else:
                xvals = np.linspace(-depth_max, -depth_min, int(abs(depth_max-depth_min)/yincr))
                
                yinterp = np.interp(xvals, np.asarray(xp), np.asarray(yp))

                var_int = yinterp[::-1] 
                for l in var_int:
                    mesh_np[counter,i]=l
                    counter= counter+1

        else:
            pass
  
print len(fnoutcollector),len(snoutcollector), len(line_points)



y_tick = []
y_label = []
x_tick = []
x_label = []
grid_depth=round(round(float(str(dep*yincr))/(10**(len(str(int(dep*yincr)))-2))))*10**(len(str(int(dep*yincr)))-2)
grid_min=round(round(float(str(min_depth))/(10**(len(str(int(min_depth)))-2))))*10**(len(str(int(min_depth)))-2)
print grid_depth, dep
#step = round(grid_depth/20.)
if len(vert) > 1:
    for v in vert:
        print v
        x_tick.append(v[3])
        x_label.append('('+str(int(round(v[1])))+','+str(int(round(v[2])))+')')
else:
    pass

                
for v in np.linspace(grid_min,grid_min+grid_depth, num = 21):
    print v
    y_tick.append((v-grid_min)/yincr)
    y_label.append(str(-int(v)))

fig_mesh_np,ax_mesh_np = plt.subplots()
ax_mesh_np.set_yticks(y_tick)
ax_mesh_np.set_yticklabels(y_label)

ax_mesh_np.set_xticks(x_tick)
ax_mesh_np.set_xticklabels(x_label)
ax_mesh_np.xaxis.grid(True)
ax_mesh_np.yaxis.grid(True)
plt.xticks(rotation=30)
ax_mesh_np = plt.gca()
ax_mesh_np.invert_yaxis()
mesh_masked = ma.masked_outside(mesh_np, -1e+30,1e+30)
if args.contourf=="yes":
    pm=plt.contourf(mesh_masked, cmap=cmap);plt.colorbar()           
else:
    #pm=plt.pcolormesh(mesh_masked, cmap=cmap);plt.colorbar()
    pm=plt.pcolormesh(mesh_masked, cmap=cmap);plt.colorbar()
plt.title(args.variable+' '+ date_time(meta[1][args.time]))
plt.axis('tight')

#line plot
fig_map, ax_map = plt.subplots()
#p=plt.imshow(mx[int(float(args.yzoom.split(':')[0])*mx.shape[0]/100.):int(float(args.yzoom.split(':')[1])*mx.shape[0]/100.), int(float(args.xzoom.split(':')[0])*mx.shape[1]/100.):int(float(args.xzoom.split(':')[1])*mx.shape[1]/100.)], cmap=cmap, origin='lower', interpolation='nearest');plt.colorbar()     
p=plt.pcolormesh(mx[int(float(args.yzoom.split(':')[0])*mx.shape[0]/100.):int(float(args.yzoom.split(':')[1])*mx.shape[0]/100.), int(float(args.xzoom.split(':')[0])*mx.shape[1]/100.):int(float(args.xzoom.split(':')[1])*mx.shape[1]/100.)], cmap=cmap);plt.colorbar()     
if args.var_min or args.var_max:
     if args.var_min and args.var_max:
          if args.var_min < args.var_max:
               pm.set_clim(float(args.var_min), float(args.var_max))
          else:
               print 'incorrect var_min shoud be less than var_max, defaults then'
               pass
     else:
          pm.set_clim(args.var_min, args.var_max)
else:
     pass
plt.axis('tight')


xl=[]
yl=[]
for i in line_points:
    xl.append(i[1])
    yl.append(i[0])
plt.plot(yl, xl,'co', markersize=2)

#format axes





plt.show()



                


