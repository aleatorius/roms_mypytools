 #!/usr/bin/env python 
##!/home/ntnu/mitya/virt_env/virt1/bin/python -B
## Dmitry Shcherbin, 2014.12.05
import numpy as np
from numpy import *
from netCDF4 import *
import sys, re, glob, os
import numpy.ma as ma
import argparse
import os.path
import datetime
from datetime import date, time
from matplotlib.path import Path

parser = argparse.ArgumentParser(
description='polygon zoom'
)

parser.add_argument(
'--ref_datetime', 
help='reference date time: 1970-01-01 00:00:00', 
dest='ref_datetime', 
action="store", 
nargs=2, 
default=None
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
'-i', 
help='input file', 
dest='inf', 
action="store"
)
parser.add_argument(
'-v', 
help='variable', 
dest ='variable', 
action="store"
)
parser.add_argument(
'--f', 
help='time format - seconds or days with respect to reference date and time', 
dest='time_f', 
action="store",
choices=("s","d"), 
default="s"
)
parser.add_argument(
'--time_rec', 
help='time records name - ocean_time, clim_time, time, etc', 
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
help='zoom along x direction, range is defined in percents', 
dest ='xzoom', 
action="store",  
default='0:100'
)
parser.add_argument(
'--yzoom', 
help='zoom along y direction, range is defined in percents', 
dest ='yzoom', 
action="store",  
default='0:100'
)
parser.add_argument(
'--xrange', 
help='zoom along x direction', 
dest ='xrange', 
action="store",  
default=None
)
parser.add_argument(
'--yrange', 
help='zoom along y direction', 
dest ='yrange', 
action="store",  
default=None
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
help='max value of variable', 
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
if args.xrange != None:
    if ':' not in list(args.xrange):
        parser.error('provide zoom in i:k format!')
    else:
        pass
else:
    pass
if args.yrange != None:
    if ':' not in list(args.yrange):
        parser.error('provide zoom in i:k format!')
    else:
        pass
else:
    pass

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
    if args.ref_datetime == None:
        ref = date(1970,01,01)
        ref_time = time(0,0,0)
    else:
        print args.ref_datetime[0], args.ref_datetime[1]
        ref = datetime.datetime.strptime(args.ref_datetime[0],'%Y-%m-%d').date()
        ref_time = datetime.datetime.strptime(args.ref_datetime[1],'%H:%M:%S').time()

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
    f = inf
    #list of possible names in tuples
    coords = (("lat_rho","lon_rho"),("lat", "lon"))
    result = False
    for t in coords:
        try:
            print t
            lat = unpack(f.variables[str(t[0])])  
            lon = unpack(f.variables[str(t[1])])  
            result = True
            break
        except KeyError:
             #e = sys.exc_info()[0]
            print "key error, trying another name for time record"
            continue
    print result
    if result == False:
        print "there are no coordinates with names", coords

    return lat, lon
def extract(inf, variable, time, vert):
     f = inf
     if str(variable) in f.variables.keys():
          #print '\n In the file', inf
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
         exit()
     else:
         pass

     return ncvar, ot


def extract_vert(inf, inv):
#just for cs_r cs_w
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
         exit()
     else:
         pass

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


#event handler - original sample is taken from matplotlib examples (LineBuilder event handler)

class LineBuilder:
    def __init__(self, line, mx, lat, lon, x_0, y_0):
        self.line = line
        self.mx = mx
        self.lat = lat
        self.lon = lon
        self.x_0 = x_0
        self.y_0 = y_0
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
            vertices=zip(self.xs,self.ys)
            if len(self.xs) > 1:
                cycle=vertices
                cycle.append((self.xs[0],self.ys[0]))
                fig_line = plt.figure(figsize=(22, 8))
                ax_line = fig_line.add_subplot(121)
              
                lat_vert, lon_vert,vert,ncv,absx,lx,ly =[],[],[],[],[],[],[]
                label_vert=[]
                #---------------Line plot----------------------------
                for i in range(0,len(self.xs)):
                    points=get_line(int(round(cycle[i][0])), int(round(cycle[i][1])), int(round(cycle[i+1][0])),int(round(cycle[i+1][1])))
                    for j in points:
                        lx.append(j[0])
                        ly.append(j[1])
                        ncv.append(self.mx[j[1],j[0]])
                        lat_vert.append(self.lat[j[1],j[0]])
                        lon_vert.append(self.lon[j[1],j[0]])
                        if len(lx) ==1:
                            absx.append(lx[0])
                        else:
                            absx.append(absx[-1]+int(sqrt((lx[-1]-lx[-2])**2+(ly[-1]-ly[-2])**2)))
                    if len(vert)==0:
                        vert.append((absx[0],lat_vert[0],lon_vert[0]))
                        vert.append((absx[-1],lat_vert[-1],lon_vert[-1]))
                    else:
                        vert.append((absx[-1],lat_vert[-1],lon_vert[-1]))

                #Line plot parameters and line plot itself

                ncv = np.asarray(ncv)
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
                        x_label.append('('+str('%.1f' % v[1])+','+str('%.1f' % v[2])+')')
              
                else:
                    pass
                ax_line.set_xticks(x_tick)
                ax_line.set_xticklabels(x_label, rotation=30, fontsize=8)
                ax_line.xaxis.grid(True)
                ax_line.yaxis.grid(True)
                ax_line.plot(absx,ncv)




                # Polygon mask
                mask_polygon = np.zeros(( np.amax(np.asarray(ly))-np.amin(np.asarray(ly))+1, np.amax(np.asarray(lx))-np.amin(np.asarray(lx))+1))
                poly_vert=[]
                for i in vertices:
                    poly_vert.append((i[1]-np.amin(np.asarray(ly)),i[0]-np.amin(np.asarray(lx))))
            
                path = Path(poly_vert)
                mx_slice = mx[(min(np.asarray(ly))-1):(max(np.asarray(ly))), (min(np.asarray(lx))-1):(max(np.asarray(lx)))]
                for index, val in np.ndenumerate(mx_slice):
                    if path.contains_point(index)==1:
                        mask_polygon[index]=1
                    else:
                        pass

                #polygon plot
                ax_zoom = fig_line.add_subplot(122)
                x_tick, y_tick, x_label, y_label = [],[],[],[]
                for v in np.linspace(0,  np.amax(np.asarray(ly))-np.amin(np.asarray(ly)), num = 21):
                    y_tick.append(v)
                    y_label.append(str(int(y_0+v+ np.amin(np.asarray(ly)))))
                for v in np.linspace(0,  np.amax(np.asarray(lx))-np.amin(np.asarray(lx)), num = 21):
                    x_tick.append(v)
                    x_label.append(str(int(x_0+v+ np.amin(np.asarray(lx)))))
                ax_zoom.set_xticks(x_tick)
                ax_zoom.set_xticklabels(x_label, rotation=30)
                ax_zoom.set_yticks(y_tick)
                ax_zoom.set_yticklabels(y_label)
                mx_slice_masked = ma.masked_where(mask_polygon==0,mx_slice)
                mx_slice_out = ma.masked_where(mask_polygon==1,mx_slice)
                lvls = np.linspace(np.amin(mx_slice_masked),np.amax(mx_slice_masked),num=21)
                print "the following arguments can be passed to the script for further zooming if needed:"
                print "--yrange ", str(y_0+min(np.asarray(ly)))+":"+str(y_0+max(np.asarray(ly))), " --xrange ", str(x_0+min(np.asarray(lx)))+":"+str(x_0+max(np.asarray(lx))), " --var_min ", np.amin(mx_slice_masked), " --var_max ", np.amax(mx_slice_masked)
                cmap_zoom=plt.cm.spectral 
                cmap_out = plt.cm.Greys

                if args.contourf == "yes":
                    slice_mesh=ax_zoom.contourf(mx_slice_masked,levels=lvls, cmap=cmap_zoom)
                    slice_mesh_out=ax_zoom.contourf(mx_slice_out,levels=lvls, cmap=cmap_out, vmin=np.amin(mx_slice_masked), vmax=np.amax(mx_slice_masked))
                else:
                    slice_mesh=ax_zoom.pcolormesh(mx_slice_masked, cmap=cmap_zoom)
                    slice_out=ax_zoom.pcolormesh(mx_slice_out, cmap=cmap_out, vmin=np.amin(mx_slice_masked), vmax=np.amax(mx_slice_masked))
                for vert in vertices:
                    txt = plt.text(round(vert[0])-min(np.asarray(lx)), round(vert[1])-min(np.asarray(ly)), "("+str('%.1f' %  lat[(round(vert[1]),round(vert[0]))])+","+str('%.1f' % lon[(round(vert[1]),round(vert[0]))])+")", fontsize=8)
                    txt.set_bbox(dict(color='white', alpha=0.5, edgecolor='red'))

                plt.axis('tight')
                # info at polygon vertices 
                box = ax_zoom.get_position()
                ax_zoom.set_position([box.x0*1.05, box.y0, box.width, box.height])
                axColor = plt.axes([box.x0 + box.width * 1.16, box.y0, 0.01, box.height])
                plt.colorbar(slice_mesh, cax = axColor, ticks=lvls, orientation="vertical")

                #nullify arrays for next pick
                self.xs = []
                self.ys = []
                plt.show()

            else:
                print "click one more time please!"
            
        if event.dblclick ==  True:
            print "double click detected"
            line.figure.canvas.mpl_disconnect(self.cid)
            exit()


#extract data from netcdf
f = Dataset(args.inf)
meta = extract(f, args.variable, args.time, args.vert)
ncvar = meta[0]
meta_trans = extract_vertical(f, args.variable, args.time)[0]

ze =  extract(f, "zeta", args.time, args.vert)[0]
mask_rho =  extract(f, "mask_rho", args.time, args.vert)[0]
zeta = ma.masked_outside(ze, -1e+36,1e+36)
Cs_r = extract_vert(f, 'Cs_r')
s_rho = extract_vert(f, 's_rho')
Cs_w = extract_vert(f, 'Cs_w')
s_w = extract_vert(f, 's_w')
Vtransform = extract_vert(f, 'Vtransform')
#Vstretching = extract_vert(args.inf, 'Vstretching')
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


try:
    lat, lon = extract_lat_lon(f)
except:
    print "no lat lon coordinates with names lat_rho and lon_rho in this file, putting zeros"
    lat_meta, lon_meta=np.zeros(ncvar.shape), np.zeros(ncvar.shape)
f.close()

mx_trans = ma.masked_outside(meta_trans, -1e+36,1e+36)

for index, val in np.ndenumerate(mx_slice):
    






if args.xrange != None or args.yrange != None :
    x_range="0:"+str(ncvar.shape[1])
    y_range="0:"+str(ncvar.shape[0])
    if args.xrange != None and args.yrange != None :
        x_range = args.xrange
        y_range = args.yrange
 
    else:
        if args.xrange == None:
            y_range = args.yrange
        else:
            x_range = args.xrange

else:
        x_range = str(int(float(args.xzoom.split(':')[0])*ncvar.shape[1]/100.))+":"+str(int(float(args.xzoom.split(':')[1])*ncvar.shape[1]/100.))
        y_range = str(int(float(args.yzoom.split(':')[0])*ncvar.shape[0]/100.))+":"+str(int(float(args.yzoom.split(':')[1])*ncvar.shape[0]/100.))

x_0 = int(float(x_range.split(':')[0]))
y_0 = int(float(y_range.split(':')[0]))
lat = lat_meta[int(float(y_range.split(':')[0])):int(float(y_range.split(':')[1])), int(float(x_range.split(':')[0])):int(float(x_range.split(':')[1]))]
lon = lon_meta[int(float(y_range.split(':')[0])):int(float(y_range.split(':')[1])), int(float(x_range.split(':')[0])):int(float(x_range.split(':')[1]))]

fillval = 1e+36
mx = ma.masked_outside(ncvar, -fillval,fillval)[int(float(y_range.split(':')[0])):int(float(y_range.split(':')[1])), int(float(x_range.split(':')[0])):int(float(x_range.split(':')[1]))]


import matplotlib.pyplot as plt
from pylab import *
from matplotlib import colors, cm

cmap=plt.cm.spectral
fig_main, ax_main = plt.subplots()

#main plot
try:
    p=plt.imshow(mx, cmap=cmap, origin='lower', interpolation='nearest');plt.colorbar()     
except ValueError:
    e = sys.exc_info()[0]
    print e
    print "ERROR: possibly out of range: xrange yrange"
    print "yrange should be within : ", ncvar.shape[0]
    print "xrange should be within : ", ncvar.shape[1]
    print "your range for xrange :", args.xrange
    print "your range for yrange :", args.yrange

    sys.exit()


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

x_tick, y_tick, x_label, y_label = [],[],[],[]
for v in np.linspace(0,  int(y_range.split(':')[1])-y_0-1, num = 11):
    y_tick.append(v)
    y_label.append(str(int(y_0+v)))
for v in np.linspace(0,  int(x_range.split(':')[1])-x_0-1, num = 11):
    x_tick.append(v)
    x_label.append(str(int(x_0+v)))
ax_main.set_xticks(x_tick)
ax_main.set_xticklabels(x_label, rotation=30)
ax_main.set_yticks(y_tick)
ax_main.set_yticklabels(y_label)

plt.axis('tight')
ax_main.set_title(args.variable+' '+ date_time(meta[1][args.time]))


#ax = fig_main.add_subplot(111)

#line, = ax.plot([], [])  # empty line 

#linebuilder = LineBuilder(line, mx, lat, lon, x_0, y_0)


#plt.show()
