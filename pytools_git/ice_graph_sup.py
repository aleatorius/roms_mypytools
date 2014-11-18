#!/home/mitya/testenv/bin/python -B
import numpy as np
from numpy import *
from netCDF4 import *
import sys, re, glob
from os import system
import numpy.ma as ma
import datetime
from datetime import date
import argparse

parser = argparse.ArgumentParser(description='pyview 0.1')
parser.add_argument('-i', help='input file', dest='input', action="store")
#parser.add_argument('-o', help='output file', dest='output', action="store")
args = parser.parse_args()

def get_data(input, resolution):
	inp_file = open(input, "r")
	otime = []
	ice_vol =[]
	for line in inp_file.readlines():
		st = line.split()         
		otime.append(st[0])
		ice_vol.append(float(st[1])*float(resolution)*float(resolution))
	inp_file.close()
	return otime, ice_vol


def hisdate(his):
     ref=date(1970,01,01)
     outdate = (ref + datetime.timedelta(float(int(his))/(3600*24))).strftime("%Y_%m_%d")
     return outdate




otime, ice_vol = get_data(args.input,4)
xotime = [datetime.datetime.strptime(d,'%Y_%m_%d').date() for d in otime]
otime1, ice_vol1 = get_data(args.input+'.old',4)
#print otime1
xotime1 = [datetime.datetime.strptime(d,'%Y_%m_%d').date() for d in otime1]
otime2, ice_vol2 = get_data(args.input+'.20',20)
xotime2 = [datetime.datetime.strptime(d,'%Y_%m_%d').date() for d in otime2]
#print otime2
diff = []
difftime = []
for i,k in enumerate(otime1):
	for j,l in enumerate(otime):
		if k == l:
			print k,l
			diff.append(ice_vol1[i]-ice_vol[j])
			difftime.append(k)
		else:
			pass
print difftime					 
print len(diff), len(difftime)			
xdiff = [datetime.datetime.strptime(d,'%Y_%m_%d').date() for d in difftime]

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pylab
from pylab import savefig
legend = ['diff 4km - 20km','jens ice.in', '20km run, jens ice.in']
datemin = date(1993,01,01)
datemax = date(1998,01,01)
fig = plt.figure(figsize=(10, 6))
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y_%m_%d'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=62))
plt.gca().set_xlim(datemin, datemax)
plt.plot(xdiff,diff, 'mo', markersize=1)
plt.plot(xotime,ice_vol, 'ro', markersize=3)
plt.plot(xotime1,ice_vol1, 'bo', markersize=2)
#plt.plot(xotime2,ice_vol2, 'yo', markersize=1)
plt.legend(legend, loc='upper left')
plt.title('Ice volume, arctic 4km')
plt.gcf().autofmt_xdate()
#pylab.savefig('ice_volume.png')


plt.show()
