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
		ice_vol.append(float(st[-2])*float(resolution)*float(resolution))
	inp_file.close()
	return otime, ice_vol


def hisdate(his):
     ref=date(1970,01,01)
     outdate = (ref + datetime.timedelta(float(int(his))/(3600*24))).strftime("%Y_%m_%d")
     return outdate


import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pylab
from pylab import savefig
from matplotlib.ticker import FormatStrFormatter, FuncFormatter
datemin = date(2005,01,01)
datemax = date(2007,01,01)
#ymin = -2.e7
#ymax= 6.e7
fig = plt.figure(figsize=(20, 8))

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
#plt.gca().yaxis.set_minor_formatter(FormatStrFormatter("%.2f"))
#plt.gca().yaxis.set_minor_formatter(FuncFormatter(lambda x, pos: ('%.2f')%(x*1e-7)))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=40))
plt.gca().set_xlim(datemin, datemax)
plt.gcf().autofmt_xdate()
plt.grid()
#plt.gca().set_ylim(31, 35)
#plt.gca().yaxis.tick_right()



data0 = otime0, bio_vol0 = get_data("aice_kong",1)


bio_vol0=np.asarray(bio_vol0)
xotime0 = [datetime.datetime.strptime(d,'%Y-%m-%d').date() for d in otime0]
max_bio0 = max(bio_vol0)
bio_vol0= bio_vol0#/max_bio0
plt.plot(xotime0,bio_vol0, "b")
plt.show()
sys.exit()
ranges=['0_50','50_100','100_200']
runs=["oldrun", "rerun"]
legend=[]
for run in runs:
	for depth in ranges:
		legend.append(run+" "+depth)
		if run == "oldrun":
			color = "b"
		else:
			color = "r"

		if depth == "0_50":
			pass
		elif depth == "50_100":
			color= color+"--"
		else:
			color=color+"-."
		



plt.legend(legend, loc='best')
plt.show()
sys.exit()
data1 = otime1, bio_vol1 = get_data(bio[0]+args.input,1)
#print otime1
xotime1 = [datetime.datetime.strptime(d,'%Y-%m-%d').date() for d in otime1]
bio_vol1=np.asarray(bio_vol1)
max_bio1 = max(bio_vol1)
bio_vol1= bio_vol1/max_bio1

data2 = otime2, bio_vol2 = get_data(bio[1]+args.input,1)
xotime2 = [datetime.datetime.strptime(d,'%Y-%m-%d').date() for d in otime2]
bio_vol2=np.asarray(bio_vol2)
max_bio2 = max(bio_vol2)
bio_vol2= bio_vol2/max_bio1
#print otime2
data3 = otime3, bio_vol3 = get_data(bio[2]+args.input,1)
xotime3 = [datetime.datetime.strptime(d,'%Y-%m-%d').date() for d in otime3]
bio_vol3=np.asarray(bio_vol3)
max_bio3 = max(bio_vol3)
bio_vol3= bio_vol3/max_bio1

#diff01 = diffplot(data0, data1) 
#xdiff01 = [datetime.datetime.strptime(d,'%Y_%m_%d').date() for d in diff01[0]]
#diff02 = diffplot(data0, data2) 
#xdiff02 = [datetime.datetime.strptime(d,'%Y_%m_%d').date() for d in diff02[0]]

#legend = ['jens ice.in, 4km', 'old ice.in, 4km', '20km run, Nils ice.in', 'diff Jens ice.in 4km - old apn ice.in 4km', 'diff Jens ice.in 4km - Nils ice.in 20km']
legend = []
counter=0
max_bio=[max_bio1,max_bio2,max_bio3]
for i in bio:
	legend.append(str(i)+" max val: "+str(max_bio[counter]))
	counter=counter+1
	
#plt.plot(xotime0,bio_vol0, 'r')

plt.plot(xotime2,bio_vol2, 'k')
plt.plot(xotime3,bio_vol3, 'm')

#plt.plot(xotime0,bio_vol0, 'ro', markersize=3)
#plt.plot(xotime1,bio_vol1, 'bo', markersize=2)
#plt.plot(xotime2,bio_vol2, 'ko', markersize=1)
#plt.plot(xotime3,bio_vol3, 'mo', markersize=2)
#plt.plot(xdiff02,diff02[1], 'ro', markersize=1)


plt.title('biomass')

#plt.gca().set_yticks([-1.5e7,-1.25e7,-0.75e7,-0.5e7,-0.25e7,0.25e7,0.5e7, 0.75e7, 2.25e7, 2.5e7,2.75e7, 3.25e7, 3.5e7], minor=True)
#plt.gca().set_yticks([-0.5e7,0.25e7,0.5e7], minor=True)
plt.gca().yaxis.grid(True, which='minor', linewidth=1)
#plt.gca().yaxis.grid(True, which='minor')


#pylab.savefig('ice_volume.png')

fig1 = plt.figure(figsize=(20, 8))
legend = ['NO3']
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
#plt.gca().yaxis.set_minor_formatter(FormatStrFormatter("%.2f"))
plt.gca().yaxis.set_minor_formatter(FuncFormatter(lambda x, pos: ('%.2f')%(x*1e-7)))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=40))
plt.gca().set_xlim(datemin, datemax)
#plt.gca().set_ylim(0, 2)
plt.gca().yaxis.tick_right()
plt.plot(xotime0,bio_vol0, 'r')
#plt.plot(xotime1,bio_vol1, 'b')
#plt.plot(xotime2,bio_vol2, 'k')
#plt.plot(xotime3,bio_vol3, 'm')

#plt.plot(xotime0,bio_vol0, 'ro', markersize=3)
#plt.plot(xotime1,bio_vol1, 'bo', markersize=2)
#plt.plot(xotime2,bio_vol2, 'ko', markersize=1)
#plt.plot(xotime3,bio_vol3, 'mo', markersize=2)
#plt.plot(xdiff02,diff02[1], 'ro', markersize=1)

plt.legend(legend, loc='upper left')
plt.title('NO3')

#plt.gca().set_yticks([-1.5e7,-1.25e7,-0.75e7,-0.5e7,-0.25e7,0.25e7,0.5e7, 0.75e7, 2.25e7, 2.5e7,2.75e7, 3.25e7, 3.5e7], minor=True)
#plt.gca().set_yticks([-0.5e7,0.25e7,0.5e7], minor=True)
plt.gca().yaxis.grid(True, which='minor', linewidth=1)
#plt.gca().yaxis.grid(True, which='minor')
plt.grid()
plt.gcf().autofmt_xdate()
#pylab.savefig('ice_volume.png')
plt.show()
