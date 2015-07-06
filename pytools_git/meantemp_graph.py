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
datemin = date(1999,07,01)
datemax = date(2001,01,01)
#ymin = -2.e7
#ymax= 6.e7
fig = plt.figure(figsize=(20, 8))

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
#plt.gca().yaxis.set_minor_formatter(FormatStrFormatter("%.2f"))
#plt.gca().yaxis.set_minor_formatter(FuncFormatter(lambda x, pos: ('%.2f')%(x*1e-7)))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=60))
plt.gca().set_xlim(datemin, datemax)
plt.gcf().autofmt_xdate()
plt.grid()
#plt.gca().set_ylim(31, 35)
#plt.gca().yaxis.tick_right()


#ranges=['0_50','50_100','100_200']
#runs=["oldrun", "rerun"]
files = [
"/global/work/mitya/rerun_1999/temp_a4_aw_rerun",
"/global/work/mitya/rerun_1999/temp_aw_a20_restored", 
"/global/work/mitya/rerun_bath20/temp_a4_aw_rerun_extra", 
"/global/work/mitya/rerun_mix/temp_mix_rerun",
"/global/work/mitya/rerun_bath4/temp_bath4"]
legend=[
"a4 rerun", 
"a20 restored", 
"bath20", 
"mix",
"cor bath4",
]
colors = ["r", "b", "g", "m","ro"]
zipped = zip(files, colors)
print zipped
for file in zipped:
	data0 = otime0, bio_vol0 = get_data(file[0],1)
	bio_vol0=np.asarray(bio_vol0)
	xotime0 = [datetime.datetime.strptime(d,'%Y-%m-%d').date() for d in otime0]
	max_bio0 = max(bio_vol0)
	bio_vol0= bio_vol0#/max_bio0
	plt.plot(xotime0,bio_vol0, file[1])


plt.legend(legend, loc='best')
plt.show()
