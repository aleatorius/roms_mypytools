#!/home/mitya/testenv/bin/python -B                                                                                                           
'''myproj.py x,y, d(i)'''
import numpy as np
from numpy import *
from netCDF4 import *
import pyproj
from pyproj import Proj
import sys, re, glob
from os import system
import matplotlib.pyplot as plt
from pylab import *
from matplotlib import colors, cm
import numpy.ma as ma

a = sys.argv
if len(a) != 6: print 'not a correct input'; print __doc__; sys.exit()
x = float(sys.argv[1])
y = float(sys.argv[2])
tr = sys.argv[3]
size_a = int(sys.argv[4])
size_s =  int(sys.argv[5])
if str(tr) not in ('i','d'): print 'not a string i (for the inverse proj-transformation) or d (for a direct one)'; print __doc__; sys.exit()
try: float(x), float(y)
except ValueError: print 'not a number'; print __doc__; sys.exit()
#try: float(y)
#except ValueError: print 'not a number'; print __doc__; sys.exit()

a = np.array([x,y])

p = Proj(proj='stere', R=6371000.0, lat_0=90, lat_ts=60.0, x_0=4180000.0, y_0=2570000.0, lon_0=58.0)
def pro(ar,s):
    if str(s)=='d':
        return np.array(p(ar[0],ar[1]))/4000.
    if str(s) == 'i':
        ar = ar*4000.
        return np.array(p(ar[0],ar[1], inverse=True))
    else:
        print 'please specify d or i'
        return


print (pro(a, tr)[0], pro(a, tr)[1])

f = Dataset('/home/mitya/models/NorROMS/Apps/Common/Grid/arctic4km_grd.nc')

mask = f.variables['mask_rho']
bath = f.variables['h']
#lon, lat  = f.variables['lon_rho'], f.variables['lat_rho']

c,h = zeros(mask.shape), zeros(bath.shape)

c[:], h[:] = mask[:], bath[:]

#st = zeros(mask.shape)
f.close()

size=size_a
cmap = plt.cm.spectral
h_masked = ma.masked_where(c==0, h)
h_slice=h_masked[(pro(a, tr)[1]-size):(pro(a, tr)[1]+size), (pro(a, tr)[0]\
-size):(pro(a, tr)[0]+size)]
print h_slice.shape


#print max(h_slice.reshape((2*size)**2,)), min(h_slice.reshape((2*size)**2,))
hmin=np.amin(h_slice)
hmax= np.amax(h_slice)
lvls= np.linspace(hmin, hmax, num = 21)
fig_mesh, ax_mesh = plt.subplots()
x_tick, y_tick, x_label, y_label = [],[],[],[]
for v in np.linspace(0, 2*size,num = 21):
    y_tick.append(v)
    y_label.append(str(int(v+int((pro(a, tr)[1]-size)))))
    x_tick.append(v)
    x_label.append(str(int(v+int((pro(a, tr)[0]-size)))))


ax_mesh.set_yticks(y_tick)
ax_mesh.set_yticklabels(y_label)
plt.xticks(rotation=30)
ax_mesh.set_xticks(x_tick)
ax_mesh.set_xticklabels(x_label)

ax_mesh.xaxis.grid(True)
ax_mesh.yaxis.grid(True)
plt.contourf(h_slice , cmap = cmap, levels= lvls);plt.colorbar(ticks=lvls)
plt.clim(hmin,hmax)
plt.plot(size, size,'ro', markersize=5)
plt.title('arctic4')
plt.axis('tight')
#plt.contour(h_slice, levels, colors = 'k', linestyles = 'solid')
plt.show(block=False)

f = Dataset('/home/mitya/models/NorROMS/Apps/Common/Grid/norseas_800m_grid.nc_Svalbard')

mask = f.variables['mask_rho']
bath = f.variables['h']
print bath.shape
lon_r, lat_r  = f.variables['lon_rho'], f.variables['lat_rho']

c,lat,lon,h = zeros(mask.shape), zeros(lat_r.shape), zeros(lon_r.shape), zeros(bath.shape)

c[:],lat[:],lon[:], h[:] = mask[:],lat_r[:],lon_r[:], bath[:]

#st = zeros(mask.shape)
f.close()
def nearly_equal(a,b,sig_fig):
    return ( a==b or 
             int(a*10**sig_fig) == int(b*10**sig_fig)
           )
#lx=[]
#ly= []
#for index, l in np.ndenumerate(lon):
#    if nearly_equal(x,l,2):
#        if nearly_equal(lat[index],y,1):
#            print l, lat[index],index
#            lx.append(index[1]), ly.append(index[0])
#        else:
#            pass
#    else:
#        pass
sx=[]
sy= []
diff=[]
index_sh = (0,0)
for index, l in np.ndenumerate(lon):
    if abs(x-l)< 0.01:
        if abs(lat[index]-y)<0.1:
            print l, lat[index],index
            sx.append(index[1]), sy.append(index[0]), diff.append(np.sqrt((x-l)**2+(lat[index]-y)**2))
        else:
            pass
    else:
        pass
index_sh = (sy[np.argmin(diff)], sx[np.argmin(diff)])
print np.amin(diff), lat[index_sh],lon[index_sh], np.sqrt((x-lon[index_sh])**2+(lat[index_sh]-y)**2) 
h_masked = ma.masked_where(c==0, h)
hmin=np.amin(h_masked)
hmax= np.amax(h_masked)
lvls= np.linspace(hmin, hmax, num = 21)
fig_sv, ax_sv = plt.subplots()
x_tick, y_tick, x_label, y_label = [],[],[],[]
plt.contourf(h_masked , cmap = cmap, levels= lvls);plt.colorbar(ticks=lvls)

ax_sv.xaxis.grid(True)
ax_sv.yaxis.grid(True)
ly,lx = [index_sh[0]],[index_sh[1]]
plt.clim(hmin,hmax)
if index_sh != (0,0):
    plt.plot(index_sh[1], index_sh[0],'ro', markersize=5)
plt.title('svalbard 800m')
plt.axis('tight')
#plt.contour(h_slice, levels, colors = 'k', linestyles = 'solid')
size=size_s
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
plt.contourf(h_slice , cmap = cmap, levels= lvls);plt.colorbar(ticks=lvls)
plt.clim(hmin_s,hmax_s)
#if len(lx)>0:
plt.plot(size, size,'ro', markersize=5)
plt.title('svalbard 800m')
plt.axis('tight')
plt.show()
