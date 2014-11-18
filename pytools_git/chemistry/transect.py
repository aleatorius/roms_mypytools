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
parser = argparse.ArgumentParser(description='pyview 0.1')

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
     f = Dataset(inf)
     if str(inv) in f.variables.keys():
          print '\n In the file', inf
          print 'variable', inv, 'exists'
          ncvar = unpack(f.variables[inv])
          print 'the grid dimensions of requested variable:', ncvar.shape

     else:
          print 'provided variable doesnt exists, choose from the list:\n'
          print_list(f.variables.keys())          
          f.close()
          sys.exit()
     f.close()
     return ncvar


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

def extract_vertical(inf, variable, time):
     f = Dataset(inf)
     if str(variable) in f.variables.keys():
          print '\n In the file', inf
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
meta_trans = extract_vertical(args.inf, args.variable, args.time)[0]

ze =  extract(args.inf, "zeta", args.time, args.vert)[0]
zeta = ma.masked_outside(ze, -1e+36,1e+36)
Cs_r = extract_vert(args.inf, 'Cs_r')
s_rho = extract_vert(args.inf, 's_rho')
Cs_w = extract_vert(args.inf, 'Cs_w')
s_w = extract_vert(args.inf, 's_w')
Vtransform = extract_vert(args.inf, 'Vtransform')
Vstretching = extract_vert(args.inf, 'Vstretching')
N = len(s_rho)
Np = len(s_w)
print Np, "Np", N, "N"
#Tcline = extract_vert(args.inf, 'Tcline')
#theta_s = extract_vert(args.inf, 'theta_s')
#theta_b = extract_vert(args.inf, 'theta_b')
hc= extract_vert(args.inf, 'hc')
#print Vtransform, Vstretching, N,Tcline, hc, theta_s, theta_b
h_m =  extract(args.inf, "h", args.time, args.vert)[0]
h = ma.masked_outside(h_m, -1e+36,1e+36)





def z_r(index,zeta,h,s_rho, hc, Cs_r,N):
    z_r = zeros((int(N)))
    for k in range(N):
        #print k
        #print h[index]
        z0 = (hc * s_rho[k] + h[index]*Cs_r[k])/(hc + h[index])
        z_r[k]  = zeta[index] + (zeta[index] + h[index])*z0
    return z_r


def z_w(index,zeta,h,s_w, hc, Cs_w,Np):
    z_w = zeros((int(Np)))
    for k in range(Np):
        #print k
        #print h[index]
        z0 = (hc * s_w[k] + h[index]*Cs_w[k])/(hc + h[index])
        z_w[k]  = zeta[index] + (zeta[index] + h[index])*z0
    return z_r
#a = z_r((100,100), zeta, h, s_rho,hc, Cs_r,N)
#print a
ncvar = meta[0]
lat, lon = extract_lat_lon(args.inf)
fillval = 1e+36
import matplotlib.pyplot as plt
from pylab import *
from matplotlib import colors, cm

#masked data
mx = ma.masked_outside(ncvar, -1e+36,1e+36)
mx_trans = ma.masked_outside(meta_trans, -1e+36,1e+36)
print "mx_trans", mx_trans.shape
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
    def __init__(self, line,mx_trans, h,zeta, s_w,hc, Cs_w,Np):
        self.line = line
        self.mx_trans = mx_trans
        self.h = h
        self.zeta = zeta
        self.s_w = s_w
        self.hc = hc
        self.Cs_w = Cs_w
        self.Np = Np
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
            self.line.set_data(self.xs, self.ys)
            self.line.figure.canvas.draw()
            if len(self.xs) > 1:
                fig_line, ax_line = plt.subplots()
                lat_vert, lon_vert,vert,ncv,absx,lx,ly =[],[],[],[],[],[],[]
                label_vert=[]
                dy= []
                ncv1=[]
                z_dict = {}
                var_dict = {}
                for i in range(self.Np):
                    z_dict[str(i)]=[]
                for i in range(self.Np-1):
                    var_dict[str(i)]=[]
                for i in range(0,len(self.xs)-1):
                    points=get_line(int(round(self.xs[i])), int(round(self.ys[i])), int(round(self.xs[i+1])),int(round(self.ys[i+1])))
                    counter= 0
                    for j in points:
                        
                        counter=counter+1
                        lx.append(j[0])
                        ly.append(j[1])
                        dz=[]
                        print self.zeta[j[1],j[0]],"zeta"
                        print self.h[j[1],j[0]],"h"
                        
                        for i in range(self.Np):
                            
                            z_dict[str(i)].append([z_r((j[1],j[0]),self.zeta, self.h, self.s_w,self.hc, self.Cs_w,self.Np)[i]])
                            print i, z_dict[str(i)][-1]
                        for i in range(self.Np-1):
                            var_dict[str(i)].append(mx_trans[i,j[1],j[0]])
                        #print z_dict[str(34)], "z-r0"
                        for i in range(1, self.Np):
                            print i, z_dict[str(i)][-1],z_dict[str(i-1)][-1], z_dict[str(i)][-1][0]-z_dict[str(i-1)][-1][0]
                            dz.append([z_dict[str(i)][-1][0]-z_dict[str(i-1)][-1][0]])
                        
                        dy.append(min(dz))
                        ncv.append(-self.h[j[1],j[0]])
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
                        
                #ax_line.axis([min(absx)-(max(absx)-min(absx))/20., max(absx)+(max(absx)-min(absx))/20., min(ncv),1]) #max(ncv)+(max(ncv)-min(ncv))/20.])
#                plt.plot(absx,ncv)
           #     print dy
                print "mindy", min(dy),min(ncv),int(round(2*abs(min(ncv))/min(dy)))
                dep =int(round(2*abs(min(ncv))/min(dy)))
                mesh = np.zeros((dep,counter))
                print mesh.shape
                
                mesh[:]=1e+37

                #for i in range(int(round(2*abs(min(ncv))/min(dy)))
                for i in range(Np-1):
                    #plt.plot(absx,z_dict[str(i)], color="r")
                    plt.plot(absx,var_dict[str(i)], color="b")
                x_tick=[]
                x_label=[]
                if len(vert) > 1:
                    for v in vert:
                        x_tick.append(v[0])
                        x_label.append('('+str(int(round(v[1])))+','+str(int(round(v[2])))+')')
              
                else:
                    pass
                plt.xticks(rotation=30)
                ax_line.set_xticks(x_tick)
                ax_line.set_xticklabels(x_label)
                ax_line.xaxis.grid(True)
                ax_line.yaxis.grid(True)
                self.xs = []
                self.ys = []
                fig_h, ax_h = plt.subplots()
                ax_h.set_xticks(x_tick)
                ax_h.set_xticklabels(x_label)
                ax_h.xaxis.grid(True)
                ax_h.yaxis.grid(True)
                ax_h.axis([min(absx)-(max(absx)-min(absx))/20., max(absx)+(max(absx)-min(absx))/20., min(ncv),1]) #max(ncv)+(max(ncv)-min(ncv))/20.])
                for i in range(self.Np):
                    plt.plot(absx,z_dict[str(i)], color="r")
                    
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
linebuilder = LineBuilder(line,mx_trans,h,zeta, s_w,hc, Cs_w,Np)




plt.title(args.variable+' '+ date_time(meta[1][args.time]))
plt.show()
