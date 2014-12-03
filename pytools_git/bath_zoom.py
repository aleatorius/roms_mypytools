#!/home/mitya/testenv/bin/python -B                                                                                                           
'''myproj.py x,y, d(i)'''
import numpy as np
from numpy import *
from netCDF4 import *
#import pyproj
#from pyproj import Proj
import sys, re, glob
from os import system
import matplotlib.pyplot as plt
from pylab import *
from matplotlib import colors, cm
import numpy.ma as ma
import argparse

parser = argparse.ArgumentParser(description='transect write 0.1')

parser.add_argument('--zoom', help='zoom around clicked point', dest='zoom', action="store", default=10, type=int)
parser.add_argument('--contourf', help='colormesh or contourf', dest='contourf', choices=("yes","no"),action="store", default="yes")

args = parser.parse_args()


f = Dataset('/home/mitya/models/NorROMS/Apps/Common/Grid/norseas_800m_grid.nc_Svalbard')

mask = f.variables['mask_rho']
bath = f.variables['h']
print bath.shape
lon_r, lat_r  = f.variables['lon_rho'], f.variables['lat_rho']

c,lat,lon,h = zeros(mask.shape), zeros(lat_r.shape), zeros(lon_r.shape), zeros(bath.shape)

c[:],lat[:],lon[:], h[:] = mask[:],lat_r[:],lon_r[:], bath[:]

#st = zeros(mask.shape)
f.close()

cmap = plt.cm.spectral
h_masked = ma.masked_where(c==0, h)
hmin=np.amin(h_masked)
hmax= np.amax(h_masked)
lvls= np.linspace(hmin, hmax, num = 21)
fig_sv, ax_sv = plt.subplots()
x_tick, y_tick, x_label, y_label = [],[],[],[]
if args.contourf=="yes":
    plt.contourf(h_masked , cmap = cmap, levels= lvls);plt.colorbar(ticks=lvls)
else:
    plt.pcolormesh(h_masked , cmap = cmap);plt.colorbar(ticks=lvls)
ax_sv.xaxis.grid(True)
ax_sv.yaxis.grid(True)

plt.clim(hmin,hmax)
plt.title('svalbard 800m')
plt.axis('tight')
size = args.zoom
txt = None
dots = None
def onclick(event):
    global txt
    global dots
    global size
    txt = plt.text(event.xdata, event.ydata, str(int(h[(event.ydata, event.xdata)])), fontsize=8)
    txt.set_bbox(dict(color='white', alpha=0.5, edgecolor='red'))
    dots = plt.plot(event.xdata, event.ydata,'ro', markersize=5)
    ly,lx = [event.ydata],[event.xdata]
    h_slice=h_masked[(ly[0]-size):(ly[0]+size), (lx[0]-size):(lx[0]+size)]

    hmin_s=np.amin(h_slice)
    hmax_s= np.amax(h_slice)
    lvls= np.linspace(hmin_s, hmax_s, num = 21)
    fig_svs, ax_svs = plt.subplots()
    x_tick, y_tick, x_label, y_label = [],[],[],[]
    for v in np.linspace(0, 2*size,num = 21):
        y_tick.append(v)
        y_label.append(str(int(v+int((ly[0]-size)))))
        x_tick.append(v)
        x_label.append(str(int(v+int((lx[0]-size)))))


    ax_svs.set_yticks(y_tick)
    ax_svs.set_yticklabels(y_label)
    plt.xticks(rotation=30)
    ax_svs.set_xticks(x_tick)
    ax_svs.set_xticklabels(x_label)

    ax_svs.xaxis.grid(True)
    ax_svs.yaxis.grid(True)
    if args.contourf=="yes":
        plt.contourf(h_slice , cmap = cmap, levels= lvls);plt.colorbar(ticks=lvls)
    else:
        plt.pcolormesh(h_slice , cmap = cmap);plt.colorbar(ticks=lvls)
    plt.clim(hmin_s,hmax_s)
    plt.plot(size, size,'ro', markersize=5)
    center_txt=plt.text(size, size, str(int(h[(event.ydata, event.xdata)]))+"\n ("+str('%.2f' % lat[(event.ydata, event.xdata)])+","+str('%.2f' %  lon[(event.ydata, event.xdata)])+")", fontsize=8)
    center_txt.set_bbox(dict(color='white', alpha=0.5, edgecolor='red'))
    plt.title('svalbard 800m')
    plt.axis('tight')
    fig_sv.canvas.draw()
    plt.show()

#def offclick(event):
#    txt.remove()
#    dots.pop(0).remove()
#    fig_sv.canvas.draw()

fig_sv.canvas.mpl_connect('button_press_event', onclick)
#fig_svs.canvas.mpl_connect('button_press_event', onclick_s) 




#plt.contour(h_slice, levels, colors = 'k', linestyles = 'solid')


plt.show()
