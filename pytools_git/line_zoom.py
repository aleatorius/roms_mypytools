#!/usr/bin/env python 
##!/home/ntnu/mitya/virt_env/virt1/bin/python -B
## Dmitry Shcherbin, 2014.10.28
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
parser = argparse.ArgumentParser(description='linezoom')

parser.add_argument('--contourf', help='colormesh or contourf', dest='contourf',choices=("yes","no"), action="store", default="no")
parser.add_argument('-i', help='input file', dest='inf', action="store")
parser.add_argument('-v', help='variable', dest ='variable', action="store")
parser.add_argument('-f', help='time format', dest='time_f', action="store", default="s")
parser.add_argument('--time_rec', help='time rec', dest ='time_rec', action="store", default="ocean_time")
parser.add_argument('--time', help='time counter', dest ='time', action="store", type=int, default=0)
parser.add_argument('--vert', help='vertical coordinate number', dest ='vert', action="store", type=int, default=34)
parser.add_argument('--xzoom', help='zoom along x(?) direction, range is defined in percents', dest ='xzoom', action="store",  default='0:100')
parser.add_argument('--yzoom', help='zoom along y(?) direction, range is defined in percents', dest ='yzoom', action="store",  default='0:100')
parser.add_argument('--var_min', help='minimum value of variable', dest ='var_min', action="store", type=float, default = None)
parser.add_argument('--var_max', help='minimum value of variable', dest ='var_max', action="store", type=float, default = None)
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
     outa = zeros(ina.shape)
     outa[:] = ina[:]
     return outa

def extract_lat_lon(inf):
    f = Dataset(inf)
    lat = unpack(f.variables["lat_rho"])
    lon = unpack(f.variables["lon_rho"])
    f.close()
    
    return lat, lon
def extract(inf, variable, time, vert):
     f = Dataset(inf)
     if str(variable) in f.variables.keys():
          print '\n In the file', inf
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
     ot = unpack(f.variables[args.time_rec])
     f.close()
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


#extract data from netcdf
meta = extract(args.inf, args.variable, args.time, args.vert)
ze =  extract(args.inf, "zeta", args.time, args.vert)[0]
zeta = ma.masked_outside(ze, -1e+36,1e+36)

h_m =  extract(args.inf, "h", args.time, args.vert)[0]
h = ma.masked_outside(h_m, -1e+36,1e+36)
ncvar = meta[0]
lat, lon = extract_lat_lon(args.inf)
fillval = 1e+36
import matplotlib.pyplot as plt
from pylab import *
from matplotlib import colors, cm

#masked data
mx = ma.masked_outside(ncvar, -1e+36,1e+36)
cmap=plt.cm.spectral
fig = plt.gcf()
#main plot
p=plt.imshow(mx[int(float(args.yzoom.split(':')[0])*mx.shape[0]/100.):int(float(args.yzoom.split(':')[1])*mx.shape[0]/100.), int(float(args.xzoom.split(':')[0])*mx.shape[1]/100.):int(float(args.xzoom.split(':')[1])*mx.shape[1]/100.)], cmap=cmap, origin='lower', interpolation='nearest');plt.colorbar()     
#p=plt.pcolormesh(mx[int(float(args.yzoom.split(':')[0])*mx.shape[0]/100.):int(float(args.yzoom.split(':')[1])*mx.shape[0]/100.), int(float(args.xzoom.split(':')[0])*mx.shape[1]/100.):int(float(args.xzoom.split(':')[1])*mx.shape[1]/100.)], cmap=cmap);plt.colorbar()     

#format axes
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


#event handler

class LineBuilder:
    def __init__(self, line, mx):
        self.line = line
        self.mx = mx
        self.xs = list(line.get_xdata())
        self.ys = list(line.get_ydata())
        self.cid = line.figure.canvas.mpl_connect('button_press_event', self)
 

    def __call__(self, event):
        print 'click', event
        if event.inaxes!=self.line.axes: return
        if event.button == 1:
            self.xs.append(event.xdata)
            self.ys.append(event.ydata)
            self.line.set_data(self.xs, self.ys)
            self.line.figure.canvas.draw()
        if  event.button == 3:
            #self.line.set_data(self.xs, self.ys)
            #self.line.figure.canvas.draw()
            vertices=zip(self.xs,self.ys)
            if len(self.xs) > 1:
                fig_line = plt.figure(figsize=(22, 8))
                ax_line = fig_line.add_subplot(121)
                ax_zoom = fig_line.add_subplot(122)
                lat_vert, lon_vert,vert,ncv,absx,lx,ly =[],[],[],[],[],[],[]
                label_vert=[]
                for i in range(0,len(self.xs)-1):
                    points=get_line(int(round(self.xs[i])), int(round(self.ys[i])), int(round(self.xs[i+1])),int(round(self.ys[i+1])))
            
                    for j in points:
                        lx.append(j[0])
                        ly.append(j[1])
                        ncv.append(self.mx[j[1],j[0]])
                        lat_vert.append(lat[j[1],j[0]])
                        lon_vert.append(lon[j[1],j[0]])
                        if len(lx) ==1:
                            absx.append(lx[0])
                        else:
                            absx.append(absx[-1]+int(sqrt((lx[-1]-lx[-2])**2+(ly[-1]-ly[-2])**2)))
                    if len(vert)==0:
                        vert.append((absx[0],lat_vert[0],lon_vert[0]))
                        vert.append((absx[-1],lat_vert[-1],lon_vert[-1]))
                    else:
                        vert.append((absx[-1],lat_vert[-1],lon_vert[-1]))
                ncv = np.asarray(ncv)
                print ncv.shape
                yx= zip(ly,lx)
                print  yx
                print min(np.asarray(ly)),  max(np.asarray(ly))
                print min(np.asarray(lx)),  max(np.asarray(lx))
                r_ncv = ncv[~np.isnan(ncv)]
                if len(r_ncv) != 0:
                    ax_line.axis([min(absx)-(max(absx)-min(absx))/20., max(absx)+(max(absx)-min(absx))/20., min(r_ncv), max(r_ncv)+(max(r_ncv)-min(r_ncv))/20.])
                else:
                    pass

                x_tick=[]
                x_label=[]
                if len(vert) > 1:
                    for v in vert:
                        x_tick.append(v[0])
                        x_label.append('('+str(int(round(v[1])))+','+str(int(round(v[2])))+')')
              
                else:
                    pass
                ax_line.set_xticks(x_tick)
                ax_line.set_xticklabels(x_label, rotation=30)
                ax_line.xaxis.grid(True)
                ax_line.yaxis.grid(True)

#                plt.xticks(rotation=30)
                ax_line.plot(absx,ncv)

                ax_zoom = fig_line.add_subplot(122)
                #plt.xticks(rotation=30)
                mx_slice = mx[(min(np.asarray(ly))-1):(max(np.asarray(ly))), (min(np.asarray(lx))-1):(max(np.asarray(lx)))]
                print mx_slice.shape
                lvls = np.linspace(np.amin(mx_slice),np.amax(mx_slice),num=21)
                cmap_zoom=plt.cm.spectral             
                if args.contourf == "yes":
                    slice_mesh=ax_zoom.contourf(mx_slice,levels=lvls, cmap=cmap_zoom)
                else:
                    slice_mesh=ax_zoom.pcolormesh(mx_slice, cmap=cmap_zoom)
                plt.colorbar(slice_mesh, ticks=lvls)
#                xl=[]
#                yl=[]
#               for i in  zip(ly,lx):
#                    xl.append(i[1])
#                    yl.append(i[0])
                ax_zoom.plot(np.asarray(lx)-min(np.asarray(lx)),np.asarray(ly)-min(np.asarray(ly)),'co', markersize=2)
                for vert in vertices:
                    txt = plt.text(round(vert[0])-min(np.asarray(lx)), round(vert[1])-min(np.asarray(ly)), "("+str('%.1f' %  lat[(round(vert[1]),round(vert[0]))])+","+str('%.1f' % lon[(round(vert[1]),round(vert[0]))])+")", fontsize=8)
                    txt.set_bbox(dict(color='white', alpha=0.5, edgecolor='red'))

                plt.axis('tight')
                

                self.xs = []
                self.ys = []
                plt.show()

            else:
                print "click one more time please!"
            
        if event.dblclick ==  True:
            print "double click detected"
            line.figure.canvas.mpl_disconnect(self.cid)
            exit()



ax = fig.add_subplot(111)
ax.set_title('click to build line segments')

line, = ax.plot([], [])  # empty line 
linebuilder = LineBuilder(line, mx)




plt.title(args.variable+' '+ date_time(meta[1][args.time]))
plt.show()
