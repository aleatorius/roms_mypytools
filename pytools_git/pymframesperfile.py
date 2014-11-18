#!/usr/bin/env python 
##!/home/ntnu/mitya/virt_env/virt1/bin/python -B
## Dmitry Shcherbin, 2014.07.01
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


import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pylab import *
from matplotlib import colors, cm
import pylab
from pylab import savefig

plt.ioff()


parser = argparse.ArgumentParser(description='frames generator, extracts snapshots from netcdf file')
parser.add_argument('-o', help='output dir', dest='dir', action="store", default='frames')
parser.add_argument('-i', help='input file', dest='input', action="store")
parser.add_argument('-v', help='variable', dest ='variable', action="store")
parser.add_argument('--time', help='time counter', dest ='time', action="store", type=int, default=0)
parser.add_argument('--vert', help='vertical coordinate number', dest ='vert', action="store", type=int, default=34)
parser.add_argument('--xzoom', help='zoom along x(?) direction, range is defined in percents', dest ='xzoom', action="store",  default='0:100')
parser.add_argument('--yzoom', help='zoom along y(?) direction, range is defined in percents', dest ='yzoom', action="store",  default='0:100')
parser.add_argument('--var_min', help='minimum value of variable', dest ='var_min', action="store", type=float, default = None)
parser.add_argument('--var_max', help='minimum value of variable', dest ='var_max', action="store", type=float, default = None)
parser.add_argument('--title', help='insert title', dest ='title', action="store", default = '')
#parser.add_argument('--title', help='insert title', dest ='title', action="store", default = '')

args = parser.parse_args()
print args.dir

if not (args.input):
    parser.error('please give an input file name')
if not os.path.isfile(args.input):
     print 'file does not exist'
     parser.error('please give an input file name')
     

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
#     ref_time = time(0,0,0)
#     refer= datetime.datetime.combine(ref, ref_time)
#     return (ref + datetime.timedelta(float(ot)/(3600*24))).strftime("%Y-%m-%d %H:%M:%S")
     return (ref + datetime.timedelta(float(ot)/(3600*24))).strftime("%Y-%m-%d")

if not (args.variable):
    f = Dataset(args.inf)
    print_list(f.variables.keys())
    f.close()
    sys.exit()


def unpack(ina):
     outa = zeros(ina.shape)
     outa[:] = ina[:]
     return outa

def extract(inf, variable, time, vert):
     f = Dataset(inf)
     if str(variable) in f.variables.keys():
          print '\n In the file', inf
          print 'variable', variable, 'exists'
          ncvar_gen = unpack(f.variables[variable][time,:])
          print 'and its dimension equals:', size(ncvar_gen.shape)+1
          if size(ncvar_gen.shape) == 3:
              ncvar = ncvar_gen[vert,:]
          if size(ncvar_gen.shape) == 2:
              ncvar = ncvar_gen
          if size(ncvar_gen.shape) == 1:
              print 'possibly there is no time dimension, so it is shown as it is'
              ncvar = unpack(f.variables[variable])
          else:
               pass
          print 'the grid dimensions of requested variable:', ncvar_gen.shape

     else:
          print 'provided variable doesnt exists, choose from the list:\n'
          print_list(f.variables.keys())          
          f.close()
          sys.exit()
     ot = unpack(f.variables['ocean_time'])
     f.close()
     return ncvar, ot

def extract_allrec(inf, variable,vert):
     f = Dataset(inf)
     if str(variable) in f.variables.keys():
          print '\n In the file', inf
          print 'variable', variable, 'exists'
          ncv = unpack(f.variables[variable])
          print 'and its dimension equals:', size(ncv.shape)+1
          if size(ncv.shape) == 4:
               ncvar = ncv[:,vert,:]
          if size(ncv.shape) == 3:
               ncvar = ncv
          if size(ncv.shape) == 2:
               print 'possibly there is no time dimension, so it is shown as it is'
               ncvar = ncv
          else:
               pass
          print 'the grid dimensions of requested variable:', ncvar.shape

     else:
          print 'provided variable doesnt exists, choose from the list:\n'
          print_list(f.variables.keys())          
          f.close()
          sys.exit()
     ot = unpack(f.variables['ocean_time'])
     f.close()
     return ncvar, ot


def snapshot(framefile):
    print 'iterator', framefile
    meta = extract_allrec(framefile, args.variable, args.vert)
    ncvar = meta[0]
    rec = 0
    for time in meta[1]:
        print time
        fig = plt.figure()
        mx = ma.masked_outside(ncvar[rec,:], -1e+36,1e+36)
        maxval = numpy.amax(mx)
        minval = numpy.amin(mx)
        print maxval, minval
 
        cmap=plt.cm.spectral
        p= plt.pcolormesh(mx[int(float(args.yzoom.split(':')[0])*mx.shape[0]/100.):int(float(args.yzoom.split(':')[1])*mx.shape[0]/100.), int(float(args.xzoom.split(':')[0])*mx.shape[1]/100.):int(float(args.xzoom.split(':')[1])*mx.shape[1]/100.)], cmap=cmap) 
        x =plt.colorbar()     
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
        plt.title(args.title +' '+ date_time(meta[1][rec])+'\n' + args.variable +': max= '+ str(maxval) + ' min = '+ str(minval))
        directory ='./'+str(args.dir)+'/'
        if os.path.isdir(directory)== False:
            os.makedirs(directory)
            print 'directory does not exist, so it is just created now', directory
        else:
            print 'directory ', directory, ' exists '

        print framefile.split('/')
        if rec in range(0,10):
            pylab.savefig(directory+args.variable+'_'+framefile.split('/')[-1].replace('.nc','_'+'0'+str(rec)+'.png'))
        else:
            pylab.savefig(directory+args.variable+'_'+framefile.split('/')[-1].replace('.nc','_'+str(rec)+'.png'))
        rec = rec +1
        print rec
    return maxval, minval

#
filename = args.input
snap = snapshot(filename)

#vmin, vmax =[],[]
#while glob.glob(str('ocean_avg_*')+ i +str('*.nc')):
#    filename= glob.glob(str('ocean_avg_*')+i+str('*.nc'))[0]
#    snap = snapshot(filename)
#    vmin.append(snap[1])
#    vmax.append(snap[0])
#    print vmin
#    print vmax
#    print numpy.amax(array(vmax)), numpy.amin(array(vmin))
#    a = int(i)
#    a = a+1
#    print a
#    if a in range(0,10):
#        i = '000'+str(a)
#    elif a in range(10,100):
#        i = '00'+str(a)
#    elif a in range(100,1000):
#        i = '0'+str(a)
#    else:
#        i = str(a)
    
#print i
#print numpy.amax(array(vmax)), numpy.amin(array(vmin))


#plt.show()
#ani.save('im.mp4', writer=writer)


