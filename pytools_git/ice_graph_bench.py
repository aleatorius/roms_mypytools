#!/usr/bin/env python 
##!/home/mitya/testenv/bin/python -B
## Dmitry Shcherbin, 2014.07.01
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




data0 = otime, bio_vol = get_data(args.input,1)
xotime = [datetime.datetime.strptime(d,'%Y_%m_%d').date() for d in otime]
#data1 = otime1, bio_vol1 = get_data(args.input+'.old',4)
#print otime1
#xotime1 = [datetime.datetime.strptime(d,'%Y_%m_%d').date() for d in otime1]
#data2 = otime2, ice_vol2 = get_data(args.input+'.20.met',20)
#xotime2 = [datetime.datetime.strptime(d,'%Y_%m_%d').date() for d in otime2]
#print otime2

def diffplot(plot1, plot2):
	diff = []
	difftime = []
	for i,k in enumerate(plot1[0]):
		for j,l in enumerate(plot2[0]):
			if k == l:
				print k,l
				diff.append(plot1[1][i]-plot2[1][j])
				difftime.append(k)
			else:
				pass
	print difftime					 
	print len(diff), len(difftime)
	return difftime, diff
#diff01 = diffplot(data0, data1) 
#xdiff01 = [datetime.datetime.strptime(d,'%Y_%m_%d').date() for d in diff01[0]]
#diff02 = diffplot(data0, data2) 
#xdiff02 = [datetime.datetime.strptime(d,'%Y_%m_%d').date() for d in diff02[0]]
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pylab
from pylab import savefig
from matplotlib.ticker import FormatStrFormatter, FuncFormatter
#legend = ['jens ice.in, 4km', 'old ice.in, 4km', '20km run, Nils ice.in', 'diff Jens ice.in 4km - old apn ice.in 4km', 'diff Jens ice.in 4km - Nils ice.in 20km']
legend = ['biomass, 20km']
datemin = date(2005,01,17)
datemax = date(2007,10,01)
#ymin = -2.e7
#ymax= 6.e7
fig = plt.figure(figsize=(20, 8))

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
#plt.gca().yaxis.set_minor_formatter(FormatStrFormatter("%.2f"))
plt.gca().yaxis.set_minor_formatter(FuncFormatter(lambda x, pos: ('%.2f')%(x*1e-7)))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=240))
plt.gca().set_xlim(datemin, datemax)
plt.gca().set_ylim(ymin, ymax)
plt.gca().yaxis.tick_right()
plt.plot(xotime,bio_vol, 'ro', markersize=3)
#plt.plot(xotime1,ice_vol1, 'bo', markersize=2)
#plt.plot(xotime2,ice_vol2, 'ko', markersize=1)
#plt.plot(xdiff01,diff01[1], 'mo', markersize=2)
#plt.plot(xdiff02,diff02[1], 'ro', markersize=1)

plt.legend(legend, loc='upper left')
plt.title('biomass')

#plt.gca().set_yticks([-1.5e7,-1.25e7,-0.75e7,-0.5e7,-0.25e7,0.25e7,0.5e7, 0.75e7, 2.25e7, 2.5e7,2.75e7, 3.25e7, 3.5e7], minor=True)
#plt.gca().set_yticks([-0.5e7,0.25e7,0.5e7], minor=True)
plt.gca().yaxis.grid(True, which='minor', linewidth=1)
#plt.gca().yaxis.grid(True, which='minor')
plt.grid()
plt.gcf().autofmt_xdate()
#pylab.savefig('ice_volume.png')


plt.show()
