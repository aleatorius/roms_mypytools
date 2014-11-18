#!/usr/bin/python -B
## Dmitry Shcherbin, 2013
#date.py s 12122222 pr date.py d 12234, if you need to change reference date - do it manually in the code. Mitya
'''usage: date.py d(s) num; d for days, s for seconds'''
import os, sys, re, glob
from os import system
import datetime
from datetime import date, time
a = sys.argv
if len(a) != 3: print 'not a correct input'; print __doc__; sys.exit()
val = sys.argv[1]
num = sys.argv[2]
if str(val) not in ('s','d'): print 'not a string s (for seconds) or d (days)'; print __doc__; sys.exit()
try: float(num)
except ValueError: print 'not a number'; print __doc__; sys.exit()
ref = date(1970,01,01)
ref_time = time(0,0,0)
refer= datetime.datetime.combine(ref, ref_time)
if str(val)=='d':
    out = (ref + datetime.timedelta(float(num))).strftime("%Y-%m-%d")
    print 'with respect to a reference date   ', str(ref), '\nthe provided date is:              ', str(out)
if str(val)=='s':
    out = (refer + datetime.timedelta(float(num)/(3600*24))).strftime("%Y-%m-%d %H:%M:%S")
    print 'with respect to a reference date   ', str(refer), '\nthe provided date is:              ', str(out)


