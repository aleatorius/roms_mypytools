#!/usr/bin/env python 
##!/home/ntnu/mitya/virt_env/virt1/bin/python -B
## Dmitry Shcherbin, 2014.11.07
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
parser.add_argument('-v', help='variable', dest ='variable', action="store")
parser.add_argument('-f', help='time format', dest='time_f', action="store", default="s")
parser.add_argument('--contourf', help='colormesh or contourf', dest='contourf', choices=("yes","no"),action="store", default="no")
parser.add_argument('--res', help='resolution, fraction of minimum distance between layers', dest='res', action="store", default=2)
parser.add_argument('--extras', help='s-layers', dest='extras',choices=('yes', 'no'), action="store", default="yes")
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
    f = inf
    lat = unpack(f.variables["lat_rho"])
    lon = unpack(f.variables["lon_rho"])
    #f.close()
    return lat, lon

def extract_vert(inf, inv):
     f = inf
     if str(inv) in f.variables.keys():
          #print '\n In the file', inf
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
     ot = unpack(f.variables[args.time_rec])
     #f.close()
     return ncvar, ot

def extract_vertical(inf, variable, time):
     f = inf
     if str(variable) in f.variables.keys():
          print 'variable', variable, 'exists'
          ncvar = unpack(f.variables[variable][time,:])
     else:
          print 'provided variable doesnt exists, choose from the list:\n'
          print_list(f.variables.keys())          
          #f.close()
          sys.exit()
     ot = unpack(f.variables[args.time_rec])
     #f.close()
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
# taken from here: Trond Kristiansen https://github.com/trondkr/romstools/tree/master/VolumeFlux
def z_r(index,zeta,h,s_rho, hc, Cs_r,N, Vtransform):
    z_r = zeros((int(N)))
    if Vtransform == 2 or Vtransform == 4:
        for k in range(N):
            z0 = (hc * s_rho[k] + h[index]*Cs_r[k])/(hc + h[index])
            z_r[k]  = zeta[index] + (zeta[index] + h[index])*z0
    elif Vtransform == 1:
        for k in range(N):
            z0 = hc * s_rho[k] + (h[index] - hc) * Cs_r[k]
            z_r[k] = z0 + zeta[index] * (1.0 + z0/h[index])
        
    return z_r


def z_w(index,zeta,h,s_w, hc, Cs_w,Np, Vtransform):
    z_w = zeros((int(Np)))
    if Vtransform == 2 or Vtransform == 4:
        for k in range(Np):
            z0 = (hc * s_w[k] + h[index]*Cs_w[k])/(hc + h[index])
            z_w[k]  = zeta[index] + (zeta[index] + h[index])*z0
    elif Vtransform == 1:
        for k in range(Np):
            z0 = hc * s_w[k] + (h[index] - hc) * Cs_w[k]
            z_w[k] = z0 + zeta[index] * (1.0 + z0/h[index])
    return z_w



#extract data from netcdf
f = Dataset(args.inf)

meta = extract(f, args.variable, args.time, args.vert)
meta_trans = extract_vertical(f, args.variable, args.time)[0]
ze =  extract(f, "zeta", args.time, args.vert)[0]
mask_rho =  extract(f, "mask_rho", args.time, args.vert)[0]
zeta = ma.masked_outside(ze, -1e+36,1e+36)
Cs_r = extract_vert(f, 'Cs_r')
s_rho = extract_vert(f, 's_rho')
Cs_w = extract_vert(f, 'Cs_w')
s_w = extract_vert(f, 's_w')
Vtransform = extract_vert(f, 'Vtransform')
print "Vtransform", Vtransform
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
fig = plt.figure(figsize=(22,8))
ax = fig.add_subplot(121)
#main plot
p=ax.imshow(mx[int(float(args.yzoom.split(':')[0])*mx.shape[0]/100.):int(float(args.yzoom.split(':')[1])*mx.shape[0]/100.), int(float(args.xzoom.split(':')[0])*mx.shape[1]/100.):int(float(args.xzoom.split(':')[1])*mx.shape[1]/100.)], cmap=cmap, origin='lower', interpolation='nearest');plt.colorbar(p)     
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
    def __init__(self, line, mx_trans, h,zeta, s_w,hc, Cs_w, Np, mask_rho, s_rho, Cs_r, N, Vtransform):
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
        self.mask_rho = mask_rho
        self.s_rho = s_rho
        self.Cs_r = Cs_r
        self.N = N
        self.Vtransform = Vtransform
        self.cid = line.figure.canvas.mpl_connect('button_press_event', self)
 

    def __call__(self, event):
        global ax_tran
        global pm
        global cb
        print 'click', event
        if event.inaxes!=self.line.axes: return
        if event.button == 1:
            self.xs.append(event.xdata)
            self.ys.append(event.ydata)
            self.line.set_data(self.xs, self.ys)
            self.line.figure.canvas.draw()
        if  event.dblclick ==  True:
            self.line.set_data(self.xs, self.ys)
            self.line.figure.canvas.draw()
            if len(self.xs) > 1:
                column,lat_vert,lon_vert,vert,absx,lx,ly =[],[],[],[],[],[],[]
                dy= []
                z_dict = {}
                zr_dict = {}
                var_dict = {}
                #for i in range(self.Np):
                #    z_dict[str(i)]=[]
                #for i in range(self.Np-1):
                #    var_dict[str(i)]=[]
                line_points=[]
                counter= 0
                for i in range(0,len(self.xs)-1):
                    points=get_line(int(round(self.xs[i])), int(round(self.ys[i])), int(round(self.xs[i+1])),int(round(self.ys[i+1])))
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
                            #for i in range(self.Np):
                            z_dict[str(len(line_points)-1)]= z_w((j[1],j[0]),self.zeta, self.h, self.s_w, self.hc, self.Cs_w,self.Np, self.Vtransform)
                            var_dict[str(len(line_points)-1)] = mx_trans[:,j[1],j[0]]
                            zr_dict[str(len(line_points)-1)] =z_r((j[1],j[0]),self.zeta, self.h, self.s_rho,self.hc,self.Cs_r, self.N, self.Vtransform)
                            dy.append(min(np.diff(z_dict[str(len(line_points)-1)])))
                            column.append(z_w((j[1],j[0]),self.zeta, self.h, self.s_w,self.hc, self.Cs_w,self.Np, self.Vtransform)[self.Np-1]+self.h[j[1],j[0]])
#                            print "is it zero?", z_w((j[1],j[0]),self.zeta, self.h, self.s_w,self.hc, self.Cs_w,self.Np, self.Vtransform)[0]+self.h[j[1],j[0]]
#                            print "is it zero too?", z_w((j[1],j[0]),self.zeta, self.h, self.s_w,self.hc, self.Cs_w,self.Np, self.Vtransform)[Np-1], self.zeta[j[1],j[0]]
#                            print self.Cs_w
                        
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
                        

                #all segments are defined, Define mesh
                #print dy
                #print column
                #print np.isnan(dy).any()
                dy = np.asarray(dy)
                dy = dy[~numpy.isnan(dy)]
                res=args.res
                if len(dy)>0:
                    
                    yincr= min(dy)/res
                #dep =int(round(res*abs(max(column))/min(dy)))
                    column = np.asarray(column)
                    column = column[~numpy.isnan(column)]
                    
                    dep =int(abs(max(column))/yincr)
                else:
                    yincr=0.1
                    dep=100

                mesh = np.zeros((dep+10,counter+2))
                mesh[:]=1e+37

                try:
                    out_file = open('segments', "w")
                except IOError:
                    #e = sys.exc_info()[0]
                    #print e
                    print "cannot create file SEGMENTS in this directory, you don't have write permission here  - creating it in your home ~/segments"
                    out_file = open(os.path.expanduser('~/segments'), "w")

                if len(vert)==len(self.xs):
                    for i in range(len(vert)):
                        string = "("+str(int(round(self.xs[i])))+","+str(int(round(self.ys[i])))+") ("+str(vert[i][1])+","+str(vert[i][2])+")\n"
                        out_file.write(string)
                else:
                    print "error?"
                    pass
                out_file.close()
                #mesh writing    
                for i in range(len(line_points)):
                    if self.mask_rho[ly[i],lx[i]]==1:
                        counter=0
                        xp = zr_dict[str(i)]
                        yp = var_dict[str(i)]
            #            print z_dict[str(i)][0]
                        xvals = np.linspace(z_dict[str(i)][0], 0, int(abs(z_dict[str(i)][0])/yincr))
                        yinterp = np.interp(xvals, np.asarray(xp), np.asarray(yp))
                        var_int = yinterp[::-1] 
                        for l in var_int:
                            mesh[counter,i]=l
                            counter= counter+1


                    else:
                        pass

                #graphics
                if args.extras=="yes":
                    #figline, ax_line = plt.subplots()
                    x_tick=[]
                    x_label=[]
                    if len(vert) > 1:
                        for v in vert:
                            x_tick.append(v[0])
                            x_label.append('('+str(int(round(v[1])))+','+str(int(round(v[2])))+')')
                    else:
                        pass
 #                   plt.xticks(rotation=30)
                    #ax_line.set_xticks(x_tick)
                    #ax_line.set_xticklabels(x_label)
                    #ax_line.xaxis.grid(True)
                    #ax_line.yaxis.grid(True)
                    #for i in range(Np-1):
                    #    plt.plot(absx,var_dict[str(i)], color="b")
                    #plt.title(args.variable+' '+ date_time(meta[1][args.time]))


#                    fig_h, ax_h= plt.subplots()
#                    ax_h.set_xticks(x_tick)
#                    ax_h.set_xticklabels(x_label)
#                    ax_h.xaxis.grid(True)
#                    ax_h.yaxis.grid(True)
#                    ax_h.axis([min(absx)-(max(absx)-min(absx))/20., max(absx)+(max(absx)-min(absx))/20., -int(max(column))-int(max(column))/10.,0])
#                    
#                    for k in range(self.Np):
#                        sigma_level = []
##                        for l in range(len(line_points)):
#                            sigma_level.append(z_dict[str(l)][k])
##                        plt.plot(absx,sigma_level, color="r")
#                    plt.title("sigma-layers")    
                else:
                    pass

                #fig_mesh, ax_mesh = plt.subplots()
                y_tick = []
                y_label = []
                x_tick = []
                x_label = []
                grid_depth=int(round(float(str(dep*yincr))/(10**(len(str(int(dep*yincr)))-2)))+1)*10**(len(str(int(dep*yincr)))-2)
                print grid_depth, dep
                step = round(grid_depth/20.)
                
                
                if len(vert) > 1:
                    for v in vert:
                        x_tick.append(v[3])
                        x_label.append('('+str(int(round(v[1])))+','+str(int(round(v[2])))+')')
                else:
                    pass
                #for x in absx:
                #    x_tick.append(x)
                
                for v in np.arange(0,grid_depth, step):
                    y_tick.append(v/yincr)
                    y_label.append(str(-v))
                print mesh.shape[0], mesh.shape[1]
                mesh_masked = ma.masked_outside(mesh, -1e+36,1e+36)


                if args.contourf=="no":
                    fig.delaxes(fig.axes[3]) 
                    fig.delaxes(fig.axes[2])
                    ax_tran = fig.add_subplot(122)
                    pm=ax_tran.pcolormesh(mesh_masked, cmap=cmap)
                    cb = fig.colorbar(pm, ax=ax_tran)
#                    pm.set_clim(vmin=np.amin(mesh_masked),vmax=np.amax(mesh_masked))
                else:
                    fig.delaxes(fig.axes[3]) 
                    fig.delaxes(fig.axes[2])
                    ax_tran = fig.add_subplot(122)
                    pm=ax_tran.contourf(mesh_masked, cmap=cmap)
                    cb = fig.colorbar(pm, ax=ax_tran)
#                    pm=ax_tran.contourf(mesh_masked, cmap=cmap)#;plt.colorbar(pm, cax=ax_tran)          
#                ax_tran.set_xlim(0,mesh.shape[0])
#                ax_tran.set_ylim(0,mesh.shape[1]) 
                ax_tran.set_yticks(y_tick)
                ax_tran.set_yticklabels(y_label)
                ax_tran.set_xticks(x_tick)
                ax_tran.set_xticklabels(x_label)
                ax_tran.xaxis.grid(True)
                ax_tran.yaxis.grid(True)
                plt.xticks(rotation=30)
                ax_tran.invert_yaxis()
                ax_tran.set_title(args.variable+' '+ date_time(meta[1][args.time]))
                plt.axis('tight')
                #nullify xs.ys
                self.xs = []
                self.ys = []
                plt.draw()



                
                

                

            else:
                print "click twice please!"
            
       # if event.dblclick ==  True:
       #     print "double click detected"
       #     line.figure.canvas.mpl_disconnect(self.cid)
       #     exit()



ax_tran = fig.add_subplot(122)
ax_tran.set_title('click to build line segments')


pm=ax_tran.pcolormesh(np.random.rand(10,10), cmap=cmap)
cb = fig.colorbar(pm, ax=ax_tran)
line, = ax.plot([], [])  # empty line 
linebuilder = LineBuilder(line,mx_trans,h,zeta, s_w,hc, Cs_w,Np,mask_rho, s_rho, Cs_r, N, Vtransform)

ax.set_title(args.variable+' '+ date_time(meta[1][args.time]))
plt.show()
