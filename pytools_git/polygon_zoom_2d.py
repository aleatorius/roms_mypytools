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
import matplotlib.pyplot as plt
from pylab import *
from matplotlib import colors, cm
import z_coord
import vert_nosigma as vert_func

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
'-o', 
help='output file', 
dest='output', 
action="store",
default="output"
)
parser.add_argument(
'--pout', 
help='output polygon file', 
dest='pout', 
action="store",
default=None
)
parser.add_argument(
'--pin', 
help='input polygon file', 
dest='pin', 
action="store",
default=None
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
'-graphics', 
help='graphics yes or no', 
dest='graphics', 
action="store",
choices=("yes","no"), 
default="yes"
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
'-depth', 
help='depth', 
dest ='depth', 
action="store",  
default=None,
nargs=2,
type=float
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
        ref = date(1948,01,01)
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
    if ina.ndim == 0:
        print "is it scalar or 0d array?"
        outa = ina[()]
    else:
        outa = zeros(ina.shape)
        outa[:] = ina[:]
    return outa


def extract(f, variable, *dims):
    # dims should be ordered: time, vert
    # I assume 4d objects: time,vert, 2d grid
    #          3d objects: time, 2d
    #          2d objects: 2d grid, time independent - like bathymetry, mask, lat, lon
    if str(variable) in f.variables.keys():
        print 'variable', variable, 'exists'
        ncvar = unpack(f.variables[variable])
        print size(ncvar.shape), ncvar.shape 
        if len(dims) == 2:
            if size(ncvar.shape) == 4:
                ncvar = ncvar[dims]
                print ncvar.shape, "snap shot of 4d var at the surface layer"
            elif size(ncvar.shape) == 3:
                dims = list(dims)
                del dims[-1]
                ncvar = ncvar[tuple(dims)]
                print ncvar.shape, "snap shot of 3d var"
            else: 
                print variable, " is not a 4d or 3d var, so extracted as it is"
        elif len(dims) == 1:
            if size(ncvar.shape) == 4:
                ncvar = ncvar[dims]
                print ncvar.shape, "snap shot of 4d var"
            elif size(ncvar.shape) == 3:
                ncvar = ncvar[dims]
                print ncvar.shape, "snap shot of 3d var"
            else: 
                print variable, " is not a 4d or 3d var, so extracted as it is"
        else:
            pass
    else:
        print 'provided variable ',variable, ' doesnt exists, choose from the list:\n'
        print_list(f.variables.keys())          
        raise ValueError('no variable in the list')
    return ncvar




def get_line(x1, y1, x2, y2):
    # Bresenham's line algorithm (somebody' python implementation from the web)
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



def polygon_points(vertices):
    cycle=vertices
    cycle.append(vertices[0])
    lx,ly,vertex =[],[],[]
    for i in range(0,len(cycle)-1):
        points=get_line(int((cycle[i][0])), int((cycle[i][1])), int((cycle[i+1][0])),int((cycle[i+1][1])))
        for j in points:
            lx.append(j[0])
            ly.append(j[1])
            vertex.append(0)
        vertex[-1]=1
    vertex[0]=1
    return lx,ly,vertex


def var_to_polygon(mx,vertices,lx,ly):
    minx=min(np.asarray(lx))
    miny=min(np.asarray(ly))
    maxx=max(np.asarray(lx))
    maxy=max(np.asarray(ly))
    mask_polygon = np.zeros(( maxy-miny+1, maxx-minx+1 ))
    poly_vert=[]
    for i in vertices:
        poly_vert.append((i[1]-miny,i[0]-minx))
            
    path = Path(poly_vert)
    print minx,maxx, miny,maxy
    mx_slice = mx[(miny):(maxy+1), (minx):(maxx+1)]
    for index, val in np.ndenumerate(mx_slice):
        if path.contains_point(index)==1:
            mask_polygon[index]=1
        else:
            pass
    mx_slice_masked = ma.masked_where(mask_polygon==0,mx_slice)
    mx_slice_out = ma.masked_where(mask_polygon==1,mx_slice)

    return mx_slice_masked, mx_slice_out



def main():
    #extract data from netcdf
    f = Dataset(args.inf)

    try:
        mask_rho = extract(f,"mask_rho")
    except ValueError as e:
        print e.args
        sys.exit()

    try:
        ncvar = extract(f, args.variable, args.time)
    except ValueError as e:
        print e.args
        sys.exit()




    times = (args.time_rec, "time", "clim_time", "bry_time")
    result = False
    for t in times:
        try:
            print t
            current_time = extract(f,t)  
            result = True
            break
        except ValueError as e:
            print e.args
            print "key error, trying another name for time record"
            continue
    print result
    if result == False:
        print "there is no time var with names", times
        current_time = np.zeros(int(args.time)+1)
    else:
        pass
    print current_time, "time"


    

    coords = (("lat_rho","lon_rho"),("lat", "lon"))
    result = False
    for t in coords:
        try:
            print t
            lat_meta, lon_meta = extract(f, t[0]), extract(f, t[1])
            result = True
            break
        except ValueError as e:
            #e = sys.exc_info()
            print e.args
            #print "key error, trying another name for time record"
            continue
    print result
    if result == False:
        print "there are no coordinates with names", coords
        lat_meta, lon_meta=np.zeros(ncvar.shape), np.zeros(ncvar.shape)

    f.close()

    cmap=plt.cm.spectral
    #either new plot or from txt polygon
    if args.pin == None:
        print "no input segment file"
    else:
        x_0, y_0 = 0,0
        lat = lat_meta
        lon = lon_meta
        fillval = 1e+36
        mx = ma.masked_outside(ncvar, -fillval,fillval)
        try:
            file = open(args.pin,"r")
        except IOError:
            print  sys.exc_info()[0]
            print "there is no file ", args.pin, " in the current directory"
            sys.exit()
        xs,ys=[],[]
        for line in file:
            i =line.replace("(","").replace(")","").replace(","," ")
            print i.split()
            try:
                xs.append(int(float(i.split()[0])))
                ys.append(int(float(i.split()[1])))
            except:
                print "maybe an empty line"
                print line
                print xs, ys
                pass
        file.close()
        vertices=zip(xs,ys)
        if len(vertices) > 1:
            lx, ly, vertex = polygon_points(vertices)
            mx_slice_masked, mx_slice_out = var_to_polygon(mx,vertices,lx,ly)
            outfile=str(args.variable)+"_"+args.output               
            if os.path.isfile(outfile):
                print "file does exist at this time"
                out_file = open(outfile, 'a')
            else:
                print "no such file, creating one"
                out_file = open(outfile, 'w')
                
            out_file.write(str(date_time(current_time[args.time]))+" "+str(np.sum(mx_slice_masked))+" "+str(mx_slice_masked.mean())+"\n")
            out_file.close()
        else:
            print "just one point in the file ",args.pin
            print "provide more"
            sys.exit()




if __name__ == '__main__':
    main()
