#!/home/mitya/testenv/bin/python -B                                                                                                           
'''myproj.py x,y, d(i)'''
import numpy as np
from numpy import *
import pyproj
from pyproj import Proj
import sys, re, glob
from os import system
a = sys.argv
if len(a) != 4: print 'not a correct input'; print __doc__; sys.exit()
x = float(sys.argv[1])
y = float(sys.argv[2])
tr = sys.argv[3]
if str(tr) not in ('i','d'): print 'not a string i (for the inverse proj-transformation) or d (for a direct one)'; print __doc__; sys.exit()
try: float(x), float(y)
except ValueError: print 'not a number'; print __doc__; sys.exit()
#try: float(y)
#except ValueError: print 'not a number'; print __doc__; sys.exit()

a = np.array([x,y])
#"+proj=stere +R=6371000.0 +lat_0=90 +lat_ts=60.0 +x_0=4180000.0 +y_0=2570000.0 +lon_0=58.0"
p = Proj(proj='stere', R=6371000.0, lat_0=90, lat_ts=60.0, x_0=4180000.0, y_0=2570000.0, lon_0=58.0)
def pro(ar,s):
    if str(s)=='d':
        return np.array(p(ar[0],ar[1]))/20000.
    if str(s) == 'i':
        ar = ar*20000.
        return np.array(p(ar[0],ar[1], inverse=True))
    else:
        print 'please specify d or i'
        return


print (pro(a, tr)[0], pro(a, tr)[1])
