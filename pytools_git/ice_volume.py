#!/usr/bin/env python  
##!/home/mitya/testenv/bin/python -B
## Dmitry Shcherbin, 20014.07.01
import numpy as np
from numpy import *
from netCDF4 import *
import sys, re, glob
from os import system
import argparse
import numpy.ma as ma
import datetime
from datetime import date
parser = argparse.ArgumentParser(description='icevol')
parser.add_argument('-i', help='input file', dest='input', action="store")
parser.add_argument('-o', help='output file', dest='output', action="store")
args = parser.parse_args()

def hisdate(his):
     ref=date(1970,01,01)
     outdate = (ref + datetime.timedelta(float(int(his))/(3600*24))).strftime("%Y_%m_%d")
     return outdate

def grid_volume(ina, mask):
     vol = 0.
     for index, x in np.ndenumerate(ina):
          if mask[index]==1:
               vol = vol + x
          else:
               pass
     return vol

def unpack(ina):
     outa = zeros(ina.shape)
     outa[:] = ina[:]
     return outa
      
#--------------grid info
f = Dataset('/home/mitya/models/NorROMS/Apps/Common/Grid/arctic4km_grd.nc')
mask = unpack(f.variables['mask_rho'])
f.close()

def extract_allrec(inf, variable):
     f = Dataset(inf)
     if str(variable) in f.variables.keys():
          print '\n In the file', inf
          print 'variable', variable, 'exists'
          ncv = unpack(f.variables[variable])
          print 'and its dimension equals:', size(ncv.shape)+1
          print ncv.shape
     else:
          print 'provided variable doesnt exists, choose from the list:\n'
          print_list(f.variables.keys())          
          f.close()
          sys.exit()
     ot = unpack(f.variables['ocean_time'])
     f.close()
     return ncv, ot

def snapshot(framefile, variable, outfile):
    print 'file', framefile
    meta = extract_allrec(framefile, variable)
    ncvar = meta[0]
    rec = 0
    if os.path.isfile(outfile):
         print "file does exist at this time"
         out_file = open(outfile, 'a')
    else:
         print "no such file, creating one"
         out_file = open(outfile, 'w')
    
    for time in meta[1]:
        print hisdate(time)
        string =  str(hisdate(time)) +' '+ str(grid_volume(ncvar[rec,:], mask))+'\n'
        out_file.write(string)
        rec = rec +1
    out_file.close()



snap = snapshot(args.input, 'hice', args.output)

exit 
