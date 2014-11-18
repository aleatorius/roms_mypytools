#!/home/mitya/testenv/bin/python -B
import numpy as np
from numpy import *
from netCDF4 import *
import sys, re, glob, os
import numpy.ma as ma
import argparse
import os.path
import datetime
from datetime import date, time



def unpack(ina):
     outa = zeros(ina.shape)
     outa[:] = ina[:]
     return outa
def date_time(ot):
     ref = date(1970,01,01)
     ref_time = time(0,0,0)
     refer= datetime.datetime.combine(ref, ref_time)
     return (refer + datetime.timedelta(float(ot[args.time])/(3600*24))).strftime("%Y-%m-%d %H:%M:%S")

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
          print f.variables.keys()
          f.close()
          sys.exit()
     ot = unpack(f.variables['ocean_time'])
     f.close()
     return ncvar, ot

parser = argparse.ArgumentParser(description='pydiff 0.1')

parser.add_argument('-i', help='Two input files to diff', dest='inf', action="store", nargs=2)
parser.add_argument('-v', help='variable', dest ='variable', action="store")
parser.add_argument('--time', help='time counter', dest ='time', action="store", type=int, default=0)
parser.add_argument('--vert', help='vertical coordinate number', dest ='vert', action="store", type=int, default=34)
parser.add_argument('--xzoom', help='zoom along x(?) direction, range is defined in percents in i:k format, where 0<=i<k<=100', dest ='xzoom', action="store",  default='0:100')
parser.add_argument('--yzoom', help='zoom along y(?) direction, range is defined in percents in i:k format, where 0<=i<k<=100', dest ='yzoom', action="store",  default='0:100')
parser.add_argument('--var_min', help='minimum value of variable', dest ='var_min', action="store", type=float, default = None)
parser.add_argument('--var_max', help='minimum value of variable', dest ='var_max', action="store", type=float, default = None)
args = parser.parse_args()


if not (args.inf):
    parser.error('please give a file name')
for i in args.inf:
     if not os.path.isfile(i):
          print '\n A provided file',i, '\n does not exists'
          parser.error('Please give a correct file name')


if ':' not in list(args.xzoom):
     parser.error('\n Provide zoom range in i:k format! where 0<=i<k<=100')
else:
     for i in [0,1]:
          if 0 <= float(args.xzoom.split(':')[i])<= 100:
               pass
          else:
               parser.error('\n Wrong xzoom, maximum range is 0:100!')

if ':' not in list(args.yzoom):
     parser.error('provide zoom range  in i:k format! where 0<=i<k<=100')
else:
     for i in [0,1]:
          if 0 <= float(args.yzoom.split(':')[i])<= 100:
               pass
          else:
               parser.error('\n Wrong yzoom, maximum range is 0:100!')


if float(args.yzoom.split(':')[0])>= float(args.yzoom.split(':')[1]):
     parser.error(' Wrong xzoom range i:k: should be i<k')
if float(args.xzoom.split(':')[0])>= float(args.xzoom.split(':')[1]):
     parser.error('Wrong yzoom range i:k: should be  i<k')

if not (args.variable):
     for i in args.inf:
          f = Dataset(i)
          print f.variables.keys()
          f.close()     
     sys.exit()
     

##program


meta_0 = extract(args.inf[0], args.variable, args.time, args.vert)
meta_1 = extract(args.inf[1], args.variable, args.time, args.vert)

ot_0 = date_time(meta_0[1])
ot_1 = date_time(meta_1[1])


if ot_0 == ot_1:
     pass
else:
     print 'diffing for different time moments, is it ok?'
     
     


fillval = 1e+36
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from pylab import *
from matplotlib import colors, cm


#mx = ma.masked_outside(ncvar, -1e+36,1e+36)
mx_0 = ma.masked_outside(meta_0[0], -1e+36,1e+36)
mx_1 = ma.masked_outside(meta_1[0], -1e+36,1e+36)
mx = np.subtract(mx_0, mx_1)

cmap=plt.cm.spectral
fig1 = plt.figure(1)
p=plt.pcolormesh(mx[int(float(args.yzoom.split(':')[0])*mx.shape[0]/100.):int(float(args.yzoom.split(':')[1])*mx.shape[0]/100.), int(float(args.xzoom.split(':')[0])*mx.shape[1]/100.):int(float(args.xzoom.split(':')[1])*mx.shape[1]/100.)], cmap=cmap);plt.colorbar()     

if args.var_min or args.var_max:
#     print args.var_min, args.var_min
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
plt.title(args.variable +' '+  ot_0+' '+ args.inf[0].split('.')[1]+ '\n'+ ot_1 + ' '+ args.inf[1].split('.')[1])
plt.show()
