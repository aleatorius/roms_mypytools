#!/home/ntnu/mitya/virt_env/virt1/bin/python -B
import numpy as np
from numpy import *
from netCDF4 import *
import sys, re, glob
from os import system
#import xlrd
#from xlrd import open_workbook, XL_CELL_EMPTY, XL_CELL_BLANK, XL_CELL_TEXT, XL_CELL_NUMBER, cellname
#import pyproj
#from pyproj import Proj
import numpy.ma as ma
#import scipy
#import scipy.interpolate 
import datetime
from datetime import date
import argparse
parser = argparse.ArgumentParser(description='pyview 0.1')
parser.add_argument('-i', help='input file', dest='input', action="store")
parser.add_argument('-o', help='output file', dest='output', action="store", default="sample.nc")
parser.add_argument('-d', help='input date to grep', dest='grep', action="store")
parser.add_argument('-t', help='time var', dest='time_var', action="store", default="ocean_time")
parser.add_argument('-f', help='time format', dest='time_f', action="store", default="s")
#parser.add_argument('-o', help='output file', dest='output', action="store")
args = parser.parse_args()

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

def hisdate(his):
     ref=date(1970,01,01)
     if args.time_f =='s':
          outdate = (ref + datetime.timedelta(float(int(his))/(3600*24))).strftime("%Y_%m_%d")
     else:
          outdate = (ref + datetime.timedelta(float(int(his)))).strftime("%Y_%m_%d")
     return outdate


def unpack(ina):
     outa = zeros(ina.shape)
     outa[:] = ina[:]
     return outa


def extract_allrec(inf, variable):
     f = Dataset(inf)
     if str(variable) in f.variables.keys():
          print '\n In the file', inf
          print 'variable', variable, 'exists'
	  ot = unpack(f.variables[variable])
	  print ot.shape
     else:
          print 'provided variable doesnt exists, choose from the list:\n'
          print_list(f.variables.keys())          
          f.close()
          sys.exit()
     
     f.close()
     return ot



#xotime = [datetime.datetime.strptime(d,'%Y_%m_%d').date() for d in otime]
grep_time = datetime.datetime.strptime(args.grep,'%Y_%m_%d').date()
print 'you want to grep', grep_time

records = extract_allrec(args.input, args.time_var)
numrec=0
fnd = False
for rec in records:
     if datetime.datetime.strptime(hisdate(rec),'%Y_%m_%d').date()!=grep_time:
          #print hisdate(rec)
          numrec = numrec + 1
     else:
          print numrec
          fnd = True
          break

if fnd == True:
     string = 'ncks -d '+ args.time_var+','+str(numrec)+' '+args.input +' '+args.output + '_'+args.grep+'.nc'
     system(string)
else:
     print 'no entry'



