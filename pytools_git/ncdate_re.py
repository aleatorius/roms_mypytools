#!/global/apps/python/2.7.3/bin/python
##date.py s 12122222 pr date.py d 12234, if you need to change reference date - do it manually in the code. Mitya
## Dmitry Shcherbin, 2013
'''usage: date.py d(s) num; d for days, s for seconds'''
import numpy as np
from numpy import *
from netCDF4 import *
import os, sys, re, glob
from os import system
import datetime
from datetime import date
a = sys.argv
#if len(a) != 3: print 'not a correct input'; print __doc__; sys.exit()
his = sys.argv[1]
#val = sys.argv[1]
#num = sys.argv[2]
#if str(val) not in ('s','d'): print 'not a string s (for seconds) or d (days)'; print __doc__; sys.exit()
#try: float(num)
#except ValueError: print 'not a number'; print __doc__; sys.exit()
ref = date(1970,01,01)
#if str(val)=='d':
#    out = (ref + datetime.timedelta(float(num))).isoformat()
#if str(val)=='s':


f = Dataset(str(his))
#print '\n Dimensions: \n\n', f.dimensions.keys()
#print '\n Variables: \n\n', f.variables.keys()

#print f
ot = f.variables['ocean_time']
a = zeros(ot.shape)
a[:] = ot[:]
f.close()
lastdate = (ref + datetime.timedelta(float(int(a[-1]))/(3600*24))).strftime("%Y_%m_%d")
print str(int(a[0])), str(int(a[-1])), str(lastdate)
#out = (ref + datetime.timedelta(float(a[0])/(3600*24))).isoformat(),  (ref + datetime.timedelta(float(a[-1])/(3600*24))).isoformat()
#print 'with respect to a reference date ', str(ref), '\na ocean_his dates are:              ', str(out)
