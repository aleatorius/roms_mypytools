#!/home/mitya/testenv/bin/python -B
import numpy as np
from numpy import *
from netCDF4 import *
import sys, re, glob
from os import system
import argparse
parser = argparse.ArgumentParser(description='transect write 0.1')

parser.add_argument(
'-num', 
help='month', 
dest='num', 
action="store", 
type=int,
default=6
)
parser.add_argument(
'-i', 
help='input file', 
dest='inf', 
action="store"
)
args = parser.parse_args()


def onclick(event):
    if event.inaxes == ax:
        print event.inaxes
        try:
            dat = str('%.1f' % float(lat[0][(event.ydata, event.xdata)]))+" "+ str('%.1f' % float(lon[0][(event.ydata, event.xdata)]))
        except:
            dat = 'nan'
        txt = ax.text(event.xdata, event.ydata, dat , fontsize=8)
        txt.set_bbox(dict(color='white', alpha=0.5, edgecolor='red'))
        dots = ax.plot(event.xdata, event.ydata,'bo', markersize=2)
        fig.canvas.draw()
    elif  event.inaxes == bx:
        print event.inaxes
        try:
            dat = str('%.1f' % float(lat[1][(event.ydata, event.xdata)]))+" "+ str('%.1f' % float(lon[1][(event.ydata, event.xdata)]))
        except:
            dat = 'nan'
        txt = bx.text(event.xdata, event.ydata, dat , fontsize=8)
        txt.set_bbox(dict(color='white', alpha=0.5, edgecolor='red'))
        dots = bx.plot(event.xdata, event.ydata,'bo', markersize=2)
        fig.canvas.draw()

    else:
        print event.inaxes

def unpack(ina):
    if ina.ndim == 0:
        print "is it scalar or 0d array?"
        outa = ina[()]
    else:
        outa = zeros(ina.shape)
        outa[:] = ina[:]
    return outa


#grid_files = ('/home/mitya/models/NorROMS/Apps/Common/Grid/arctic4km_grd.nc','/home/mitya/models/NorROMS/Apps/Common/Grid/arctic20km_grd.nc')
grid_files = ['/home/mitya/models/NorROMS/Apps/Common/Grid/arctic4km_grd.nc']
#river_files = ('/home/mitya/models/NorROMS/Apps/Common/Include/arctic4km_rivers.nc', '/home/mitya/models/NorROMS/Apps/Common/Origfiles/A20_rivers_openBering35.nc')
#river_files = (args.inf, '/home/mitya/models/NorROMS/Apps/Common/Origfiles/A20_rivers_openBering35.nc')
river_files = [args.inf]
#salinity_files = ('/global/work/apn/Arctic-4km_results/1993_2010_jens/ocean_avg_0107_1996_06_20.nc', '/global/work/apn/Arctic-4km_results/arctic20_test/ocean_avg_0116_1996_06_19.nc')
#salinity_files = ('/global/work/apn/Arctic-4km_results/1993_2010_jens/ocean_avg_0510_2007_07_03.nc', '/global/work/apn/Arctic-4km_results/arctic20_test/ocean_avg_0118_1996_07_09.nc')
#salinity_files = ('/global/work/apn/Arctic-4km_results/1993_2010_jens/ocean_avg_0510_2007_07_03.nc', '/global/work/apn/a20LTR/ocean_avg_0323.nc')
salinity_files = ['/global/work/apn/Arctic-4km_results/1993_2010_jens/ocean_avg_0510_2007_07_03.nc']

files = zip(salinity_files, river_files)
mask = []
mask_u = []
mask_v = []
bath = []
river_e = []
river_x = []
river_transport = []
river_num = []
river_direction = []
salt = []
lat, lon = [],[]
vshape = []
river_salt = []
for i in files:
     print i
     f = Dataset(i[0])
     mask.append(unpack(f.variables['mask_rho']))
     mask_u.append(unpack(f.variables['mask_u']))
     mask_v.append(unpack(f.variables['mask_v']))
     bath.append(unpack(f.variables['h']))
     salt.append(unpack(f.variables['salt'])[0,34,:])
     lat.append(unpack(f.variables['lat_rho']))
     lon.append(unpack(f.variables['lon_rho']))
     f.close()
     f = Dataset(i[1])
     river_e.append(unpack(f.variables['river_Eposition']))
     river_x.append(unpack(f.variables['river_Xposition']))
     river_transport.append(unpack(f.variables['river_transport']))
     river_num.append(unpack(f.variables['river']))
     river_direction.append(unpack(f.variables['river_direction']))
     vshape.append(unpack(f.variables['river_Vshape']))
     river_salt.append(unpack(f.variables['river_salt']))
     f.close()

print "river positions"
print zip(river_e[0], river_x[0])

#print vshape[0].shape, vshape[1].shape
#print river_salt[0].shape, "river_shape"
#print river_salt[0][args.num-1,1,:].shape, np.sum(river_salt[0][args.num-1,:,13]), np.sum(river_salt[0][args.num-1,:,14])
#a = np.sum(vshape[0], axis = 0) 
#b = np.sum(vshape[1], axis = 0) 
#print a, a.shape
#print b, b.shape
#print mask_u[0][1201, 1600]
import matplotlib.pyplot as plt
from pylab import *
from matplotlib import colors, cm
import numpy.ma as ma

fig = plt.figure(figsize=(12,8))

palette = plt.cm.spectral
palette.set_over('k', 50.0)
counter= 0
for hplot in [1]:
    rho_x, rho_e = [],[]
    ax = fig.add_subplot(111)
    for i,j in enumerate(river_x[hplot-1]):
        print i,j
        
        if river_transport[hplot-1][args.num-1,i]>0:
            salt[hplot-1][int(river_e[hplot-1][i]),int(river_x[hplot-1][i])] = 51.0
            rho_x.append(river_x[hplot-1][i])
            rho_e.append(river_e[hplot-1][i])
        else:
            if river_direction[hplot-1][i]==0:
                salt[hplot-1][int(river_e[hplot-1][i]),int(river_x[hplot-1][i])-1] = 51.0
                rho_x.append(river_x[hplot-1][i]-1)
                rho_e.append(river_e[hplot-1][i])
            else:
                salt[hplot-1][int(river_e[hplot-1][i]-1),int(river_x[hplot-1][i])] = 51.0
                rho_x.append(river_x[hplot-1][i])
                rho_e.append(river_e[hplot-1][i]-1)
    print counter
    counter = 0
        
    p=ax.pcolormesh(ma.masked_outside(salt[hplot-1],-1e+36,1e+36), cmap=palette)
    plt.colorbar(p)
    p.set_clim(vmin=0,vmax=40)
    #delta = 1
    #plt.Rectangle((river_x[hplot-1], river_e[hplot-1]),width=delta,height=delta,color='red') 

    
    ax.plot(rho_x,rho_e,'ro', markersize=5)
    for i,j in enumerate(river_num[hplot-1]):
        if abs(river_transport[hplot-1][args.num-1,i])>0:
            if river_transport[hplot-1][args.num-1,i]>0:
                atxt=ax.text(river_x[hplot-1][i],river_e[hplot-1][i],str(int(j))+\
                                 ": mask: "+str(int(mask[hplot-1][int(river_e[hplot-1][i]),int(river_x[hplot-1][i])]))+ "\n"+\
                                 str(int(river_direction[hplot-1][i]))+" "+\
                                 str(int(river_transport[hplot-1][args.num-1,i])) + "\n"+\
                                 str(int(np.sum(river_salt[hplot-1][args.num-1,:,i])/river_salt[hplot-1].shape[1])), fontsize=8)
                atxt.set_bbox(dict(color='white', alpha=0.5, edgecolor='red'))
            else:
                if river_direction[hplot-1][i]==0:
                    atxt=ax.text(river_x[hplot-1][i]-1,river_e[hplot-1][i],str(int(j))+\
                                     ": mask: "+str(int(mask[hplot-1][int(river_e[hplot-1][i]),int(river_x[hplot-1][i])-1]))+"\n"+\
                                     str(int(river_direction[hplot-1][i]))+" "+\
                                     str(int(river_transport[hplot-1][args.num-1,i])) + "\n"+\
                                     str(int(np.sum(river_salt[hplot-1][args.num-1,:,i])/river_salt[hplot-1].shape[1])), fontsize=8)
                    atxt.set_bbox(dict(color='white', alpha=0.5, edgecolor='red'))
                else:
                    atxt=ax.text(river_x[hplot-1][i],river_e[hplot-1][i]-1,str(int(j))+\
                                     ": mask: "+str(int(mask[hplot-1][int(river_e[hplot-1][i])-1,int(river_x[hplot-1][i])]))+"\n"+\
                                     str(int(river_direction[hplot-1][i]))+" "+\
                                     str(int(river_transport[hplot-1][args.num-1,i])) + "\n"+\
                                     str(int(np.sum(river_salt[hplot-1][args.num-1,:,i])/river_salt[hplot-1].shape[1])), fontsize=8)
                    atxt.set_bbox(dict(color='white', alpha=0.5, edgecolor='red'))

        else:
            if river_transport[hplot-1][args.num-1,i]>0:
                atxt=ax.text(river_x[hplot-1][i],river_e[hplot-1][i],str(int(j)), fontsize=8)
                atxt.set_bbox(dict(color='white', alpha=0.5, edgecolor='red'))
            else:
                if river_direction[hplot-1][i]==0:
                    atxt=ax.text(river_x[hplot-1][i]-1,river_e[hplot-1][i],str(int(j)), fontsize=8)
                    atxt.set_bbox(dict(color='white', alpha=0.5, edgecolor='red'))
                else:
                    atxt=ax.text(river_x[hplot-1][i],river_e[hplot-1][i]-1,str(int(j)), fontsize=8)
                    atxt.set_bbox(dict(color='white', alpha=0.5, edgecolor='red'))
        plt.axis('tight')


ax = fig.add_subplot(111)
ax.set_title("arctic 4km month: "+ str(args.num))
#bx = fig.add_subplot(122)
#bx.set_title("arctic 20km month: "+ str(args.num))

#fig.canvas.mpl_connect('button_press_event', onclick)


plt.show()




