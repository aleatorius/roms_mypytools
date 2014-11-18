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

#excel file
wb = xlrd.open_workbook('extra.xlsx')
    
list = []

l = wb.sheet_by_index(0)

index_col = l.col(-1)

#generate list with info (lon, lat, year, station name, depth)
for j,i in enumerate(index_col):
     print j,i
     if i.ctype == XL_CELL_TEXT:
         if i.value != 'MAT':
             list.append([l.row(j)[1].value, l.row(j)[2].value,l.row(j)[3].value,l.row(j)[4].value, l.row(j)[-1].value])
print list
#read data from the grid
f = Dataset('arctic4km_grd.nc')

lon, lat, mask  = f.variables['lon_rho'], f.variables['lat_rho'], f.variables['mask_rho']
bath = f.variables['h']
c,b,a,h = zeros(mask.shape), zeros(lon.shape), zeros(lat.shape), zeros(bath.shape)

a[:], b[:], c[:], h[:] = lat[:], lon[:], mask[:], bath[:]

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
stx, sty = [], []
#pay attention that print goes just to stdout, which is worthwhile checking, but write() goes to the final station.txt file
for i in list:
     count=0
     wdup = wdup + 1
     print 'station: ', i[-1], '   lon,lat:', (int(i[1].split()[0])+float(i[1].split()[1])/60., int(i[0].split()[0])+float(i[0].split()[1])/60.), '\n'
     j = [int(i[0].split()[0])+float(i[0].split()[1])/60., int(i[1].split()[0])+float(i[1].split()[1])/60.]
     lats.append(j[0])
     lons.append(j[1])
     print 'lats,lons',lats, lons
     print 'projected', double(p(j[1], j[0]))/4000., '\n'
     index = [int(double(p(j[1], j[0]))[0]/4000.), int(double(p(j[1], j[0]))[1]/4000.)]
     stlist.append((index[1],index[0]))
     stx.append(index[1])
     sty.append(index[0])
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
