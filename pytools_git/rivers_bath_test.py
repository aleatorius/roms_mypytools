#!/home/mitya/testenv/bin/python -B
import numpy as np
from numpy import *
from netCDF4 import *
import sys, re, glob
from os import system
import xlrd
from xlrd import open_workbook, XL_CELL_EMPTY, XL_CELL_BLANK, XL_CELL_TEXT, XL_CELL_NUMBER, cellname
import pyproj
from pyproj import Proj

wb = xlrd.open_workbook('data_overview.xlsx')
    
list = []

l = wb.sheet_by_index(0)

index_col = l.col(-2)

for j,i in enumerate(index_col):
     if i.ctype == XL_CELL_TEXT:
         if i.value != 'MAT':
             list.append([l.row(j)[1].value, l.row(j)[2].value, l.row(j)[-2].value])


l = wb.sheet_by_index(1)

index_col = l.col(-1)

for j,i in enumerate(index_col):
     if i.ctype == XL_CELL_TEXT:
         list.append([l.row(j)[1].value, l.row(j)[2].value, l.row(j)[-1].value])

f = Dataset('/home/mitya/models/NorROMS/Apps/Common/Grid/arctic4km_grd.nc')

mask = f.variables['mask_rho']
bath = f.variables['h']
lon, lat  = f.variables['lon_rho'], f.variables['lat_rho']

c,b,a,h = zeros(mask.shape), zeros(lon.shape), zeros(lat.shape), zeros(bath.shape)

a[:], b[:], c[:], h[:] = lat[:], lon[:], mask[:], bath[:]

st = zeros(mask.shape)
f.close()

f = Dataset('/home/mitya/models/NorROMS/Apps/Common/Include/arctic4km_rivers.nc')
print '\n Variables: \n\n', f.variables.keys()
river_e=f.variables['river_Eposition']
print river_e
river_x=f.variables['river_Xposition']
print river_x
re,rx = zeros(river_e.shape), zeros(river_x.shape)
re[:], rx[:] = river_e[:], river_x[:]
print re
print rx
f.close()
p = Proj(proj='stere', R=6371000.0, lat_0=90, lat_ts=60.0, x_0=4180000.0, y_0=2570000.0, lon_0=58.0)

lats, lons = [],[]
stx, sty = [], []
for i in list:
     lats.append(i[0])
     lons.append(i[1])
     index = [int(double(p(i[1], i[0]))[0]/4000.), int(double(p(i[1], i[0]))[1]/4000.)]
     stx.append(index[1])
     sty.append(index[0])

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap, addcyclic
from pylab import *
from matplotlib import colors

cMap = colors.ListedColormap(['#CD5C5C','#00BFFF'])

fig1 = plt.figure(1)
print 'c.shape', c.shape
print 'h.shape', h.shape
for i,j in enumerate(c):
     for k,l in enumerate(j):
          if l == 0:
               h[i,k]=1000

plt.pcolormesh(h);plt.colorbar()
plt.plot(sty, stx,'ro', markersize=5)
plt.plot(rx, re, 'co', markersize=10)
plt.title('stations(gridmesh, arctic4)')
plt.axis('tight')
plt.contour(h, [10,20, 30,40,50,100,200, 300, 400, 500, 600, 700, 800, 900, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4300, 4500, 4700], colors = 'k', linestyles = 'solid')

#fig1 = plt.figure(2)
#for i,j in enumerate(h):
#     for k,l in enumerate(j):
#          if l >1000:
#               h[i,k]=0
#for i,j in enumerate(c):
#     for k,l in enumerate(j):
#          if l == 0:
#               h[i,k]=200

#plt.pcolormesh(h);plt.colorbar()
#plt.pcolormesh(c, cmap = cMap)
#plt.plot(sty, stx,'ro', markersize=5)
#plt.title('stations(gridmesh, arctic4)')
#plt.autoscale(enable=False, axis='both', tight=None)
#plt.axis('tight')
#plt.contour(h, [10, 30, 100,400, 300, 500, 1000,3000], colors = 'k', linestyles = 'solid')
#;plt.colorbar()
#savefig('st_bath_gridmesh_lim.png')

plt.show()

