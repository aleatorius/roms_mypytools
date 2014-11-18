#!/usr/bin/python -B
import numpy as np
from numpy import *
from netCDF4 import *
import sys, re, glob
from os import system
import xlrd
from xlrd import open_workbook, XL_CELL_EMPTY, XL_CELL_BLANK, XL_CELL_TEXT, XL_CELL_NUMBER, cellname
import pyproj
from pyproj import Proj

#excel file
wb = xlrd.open_workbook('data_overview_up.xlsx')
    
list = []

l = wb.sheet_by_index(0)

index_col = l.col(-2)

#generate list with info (lon, lat, year, station name, depth)
for j,i in enumerate(index_col):
     if i.ctype == XL_CELL_TEXT:
         if i.value != 'MAT':
             list.append([l.row(j)[1].value, l.row(j)[2].value,l.row(j)[3].value,l.row(j)[4].value, l.row(j)[-2].value])

#read data from the grid
f = Dataset('arctic4km_grd.nc')

lon, lat, mask  = f.variables['lon_rho'], f.variables['lat_rho'], f.variables['mask_rho']

c,b,a = zeros(mask.shape), zeros(lon.shape), zeros(lat.shape)

a[:], b[:], c[:] = lat[:], lon[:], mask[:]

f.close()

#define projection 

p = Proj(proj='stere', R=6371000.0, lat_0=90, lat_ts=60.0, x_0=4180000.0, y_0=2570000.0, lon_0=58.0)

#write list to a file content of which can be written directly to stations.in
lats, lons = [],[]
stlist = []
#new file
stf = open('stations.txt', 'w')
#formatted header which goes to  station.in
stf.write('POS =  GRID  FLAG      X-POS       Y-POS     COMMENT \n')
#just technical counters, bad style %-)
wdup=0
count=0
dump = []
#pay attention that print goes just to stdout, which is worthwhile checking, but write() goes to the final station.txt file
for i in list:
     count=0
     wdup = wdup + 1
     print 'station: ', i[-1], '   lon,lat:', (i[1], i[0]), '\n'
     lats.append(i[0])
     lons.append(i[1])
     print 'projected', double(p(i[1], i[0]))/4000., '\n'
     index = [int(double(p(i[1], i[0]))[0]/4000.), int(double(p(i[1], i[0]))[1]/4000.)]
     stlist.append((index[1],index[0]))
     print 'cell:', index[1],index[0], '\n'
     if wdup >= 2:
          for k in range(wdup-1):
               if stlist[wdup-1]==stlist[k]:
                    dump.append(stlist[wdup-1])
                    count= count + 1          
          if count != 0:
               stf.write(str('!        1     0        ')+str(index[0])+'          '+ str(index[1])+ '       '+ str(i[-1])+' '+str(i[2])+' '+str(i[3])+'\n')
          else:
               stf.write(str('         1     0        ')+str(index[0])+'          '+ str(index[1])+ '       '+ str(i[-1])+' '+str(i[2])+' '+str(i[3])+'\n')
     else:          
          stf.write(str('         1     0        ')+str(index[0])+'          '+ str(index[1])+ '       '+ str(i[-1])+' '+str(i[2])+' '+str(i[3])+'\n')
     print '   ',(b[index[1]+1,index[0]], a[index[1]+1,index[0]]), (b[index[1]+1,index[0]+1], a[index[1]+1,index[0]+1])
     print '   ',(b[index[1],index[0]], a[index[1],index[0]]), (b[index[1],index[0]+1], a[index[1]+1,index[0]+1]),'\n'


nodupst = set(stlist)
nodup=0
for i in nodupst:
     nodup = nodup + 1
stf.write('!The total number of stations in the database: '+str(wdup)+'\n!The number of station when duplicate coordinates are excluded: '+str(nodup))
stf.close()
