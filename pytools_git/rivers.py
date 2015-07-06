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
'-river', 
help='river number', 
dest='rivernum', 
action="store"
)

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
     f.close()
     f = Dataset(i[1])
     river_e.append(unpack(f.variables['river_Eposition']))
     river_x.append(unpack(f.variables['river_Xposition']))
     river_transport.append(unpack(f.variables['river_transport']))
     river_time.append(unpack(f.variables['river_time']))
     river_num.append(unpack(f.variables['river']))
     river_direction.append(unpack(f.variables['river_direction']))
     vshape.append(unpack(f.variables['river_Vshape']))
     river_salt.append(unpack(f.variables['river_salt']))
     f.close()


info = zip(river_num[0], river_e[0], river_x[0], river_direction[0],np.sum(river_transport[0], axis=0))

sealand = (1.0,0.0)

for index in info:
     if index[3] == 0:
          if index[4] > 0:
               if (mask[0][index[1],index[2]], mask[0][index[1],index[2]-1]) != sealand:
                    print "Error:"
                    print index
                    print (mask[0][index[1],index[2]], mask[0][index[1],index[2]-1])
                    print "_________________________________"
          else:
               if (mask[0][index[1],index[2]-1], mask[0][index[1],index[2]]) != sealand:
                    print "Error:"
                    print index
                    print (mask[0][index[1],index[2]-1], mask[0][index[1],index[2]])
                    print "_________________________________"
               
     else: 
          if index[4] > 0:
               if (mask[0][index[1],index[2]], mask[0][index[1]-1,index[2]]) != sealand:
                    print "Error:"
                    print index
                    print (mask[0][index[1],index[2]], mask[0][index[1]-1,index[2]])
                    print "_________________________________"
          else:
               if (mask[0][index[1]-1,index[2]], mask[0][index[1],index[2]]) != sealand:
                    print "Error:"
                    print index
                    print (mask[0][index[1]-1,index[2]], mask[0][index[1],index[2]])
                    print "_________________________________"
          

fig = plt.figure(figsize=(12,8))



counter= 0
for hplot in [1]:
    rho_x, rho_e = [],[]
    ax = fig.add_subplot(111)
    maxval = np.amax(bath[hplot-1])
    minval = np.amin(bath[hplot-1])
    limit = max(abs(minval), abs(maxval))

    for i,j in enumerate(river_x[hplot-1]):
        if river_transport[hplot-1][args.num-1,i]>0:
            bath[hplot-1][int(river_e[hplot-1][i]),int(river_x[hplot-1][i])] = limit+1000.
            rho_x.append(river_x[hplot-1][i])
            rho_e.append(river_e[hplot-1][i])
        else:
            if river_direction[hplot-1][i]==0:
                bath[hplot-1][int(river_e[hplot-1][i]),int(river_x[hplot-1][i])-1] = limit+1000.
                rho_x.append(river_x[hplot-1][i]-1)
                rho_e.append(river_e[hplot-1][i])
            else:
                bath[hplot-1][int(river_e[hplot-1][i])-1,int(river_x[hplot-1][i])] = limit+1000.
                rho_x.append(river_x[hplot-1][i])
                rho_e.append(river_e[hplot-1][i]-1)
    counter = 0
    palette = plt.cm.spectral
    palette.set_over('c', limit+100.)        
    p=ax.pcolormesh(ma.masked_where(mask[hplot-1]==0, bath[hplot-1]), cmap=palette)
    plt.colorbar(p)
    p.set_clim(vmin=minval,vmax=maxval)
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
ax.set_title("files: "+args.grid.split('/')[-1]+" and "+args.inf.split('/')[-1]+ "\n month: "+ str(args.num)+"\n \n")


if args.clicks=='yes':
    fig.canvas.mpl_connect('button_press_event', onclick)
else:
    pass

if args.rivernum:
    fig1 = plt.figure(figsize=(12, 8))
    river_display = None
    for i,j in enumerate(river_num[0]):
        if int(j)==int(args.rivernum):
            river_display = i
            break
        else:
            pass
    if river_display!=None:
        pass
    else:
        river_display = 0
    ax1 = fig1.add_subplot(1,1,1)
    ax1.plot([datetime.datetime.strptime(hisdate(d),'%Y_%m_%d').date() for d in river_time[0]], abs(river_transport[0][:,river_display]), 'r')
    ax1.plot([datetime.datetime.strptime(hisdate(d),'%Y_%m_%d').date() for d in river_time[0]],abs(river_transport[0][:,river_display]), 'bo', markersize=2)
    ax1.set_title("discharge rates for the river number "+str(int(river_num[0][river_display])))
    plt.xticks(rotation=30)
    xfmt = mdates.DateFormatter('%b %d')
    ax1.xaxis.set_major_formatter(xfmt)

plt.show()




