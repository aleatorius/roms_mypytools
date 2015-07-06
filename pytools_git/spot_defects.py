
#!/home/mitya/testenv/bin/python -B
import numpy as np
from numpy import *
from netCDF4 import *
import sys, re, glob
from os import system
import argparse
import datetime
from datetime import date
import matplotlib.pyplot as plt
from pylab import *
from matplotlib import colors, cm
import numpy.ma as ma
import matplotlib.dates as mdates
parser = argparse.ArgumentParser(description='transect write 0.1')




parser.add_argument(
'-i', 
help='input file', 
dest='inf', 
action="store"
)
parser.add_argument(
'-v', 
help='variable', 
dest='var', 
action="store"
)
parser.add_argument(
'-grid', 
help='input grid file', 
dest='grid', 
action="store"
)
parser.add_argument(
'-clicks', 
help='input grid file', 
dest='clicks', 
action="store",
choices=('yes', 'no'), 
default="no"
)
args = parser.parse_args()



def hisdate(his):
     ref=date(1970,01,01)
     outdate = (ref + datetime.timedelta(float(int(his)))).strftime("%Y_%m_%d")
     return outdate

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



grid_files = [args.grid]
river_files = [args.inf]


files = zip(grid_files, river_files)
mask = []
mask_u = []
mask_v = []
mask_rho = []
var = []
bath = []
river_e = []
river_x = []
river_transport = []
river_num = []
river_direction = []
river_time = []
lat, lon = [],[]
vshape = []
river_salt = []
for i in files:
     print i
     f = Dataset(i[0])
     mask.append(unpack(f.variables['mask_rho']))
     bath.append(unpack(f.variables['h']))
     lat.append(unpack(f.variables['lat_rho']))
     lon.append(unpack(f.variables['lon_rho']))
     try:
          mask_u.append(unpack(f.variables['mask_u']))
     except:
          print "no mask u"
     try:
          mask_v.append(unpack(f.variables['mask_v']))
     except:
          print "no mask v"
     try:
          mask_rho.append(unpack(f.variables['mask_rho']))
     except:
          print "no mask rho"

     f.close()
     f = Dataset(i[1])

     try:
          var.append(unpack(f.variables[args.var]))
          print var[0].shape, "var shape"

     except:
          print "no var ", args.var
     f.close()

print np.amax(var[0][0,:]), np.amin(var[0][0,:])
e_pos=[]
x_pos=[]
mask_val = []
for i,j in np.ndenumerate(ma.masked_where(mask_rho[0]==0, var[0][0,:])):
     if abs(j)>100. and mask_rho[0][i]==1:
          x_pos.append(i[0])
          e_pos.append(i[1])
          mask_val.append(mask_v[0][i])
print len(x_pos)
print mask_val
#info = zip(river_num[0], river_e[0], river_x[0], river_direction[0],np.sum(river_transport[0], axis=0))



#sealand = (1.0,0.0)

fig = plt.figure(figsize=(12,8))



counter= 0
for hplot in [1]:
    rho_x, rho_e = [],[]
    ax = fig.add_subplot(111)
    maxval = np.amax(bath[hplot-1])
    minval = np.amin(bath[hplot-1])
    limit = max(abs(minval), abs(maxval))

#    for i,j in enumerate(river_x[hplot-1]):
#        if river_transport[hplot-1][args.num-1,i]>0:
#            bath[hplot-1][int(river_e[hplot-1][i]),int(river_x[hplot-1][i])] = limit+1000.
#            rho_x.append(river_x[hplot-1][i])
#            rho_e.append(river_e[hplot-1][i])
#        else:
#            if river_direction[hplot-1][i]==0:
#                bath[hplot-1][int(river_e[hplot-1][i]),int(river_x[hplot-1][i])-1] = limit+1000.
#                rho_x.append(river_x[hplot-1][i]-1)
#                rho_e.append(river_e[hplot-1][i])
#            else:
#                bath[hplot-1][int(river_e[hplot-1][i])-1,int(river_x[hplot-1][i])] = limit+1000.
#                rho_x.append(river_x[hplot-1][i])
#                rho_e.append(river_e[hplot-1][i]-1)
#    counter = 0
    palette = plt.cm.spectral
    palette.set_over('c', limit+100.)        
    p=ax.pcolormesh(ma.masked_where(mask[hplot-1]==0, bath[hplot-1]), cmap=palette)
    plt.colorbar(p)
    p.set_clim(vmin=minval,vmax=maxval)
    ax.plot(e_pos,x_pos,'ro', markersize=5)






if args.clicks=='yes':
    fig.canvas.mpl_connect('button_press_event', onclick)
else:
    pass


plt.show()




