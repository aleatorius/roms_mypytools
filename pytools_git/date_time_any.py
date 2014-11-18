#!/usr/bin/python -B
#date.py s 12122222 pr date.py d 12234, if you need to change reference date - do it manually in the code. Mitya
'''usage: date.py d(s) num; d for days, s for seconds'''
import os, sys, re, glob
from os import system
import datetime
from datetime import date, time
a = sys.argv
print a
#if len(a) > 2: print 'not a correct input'; print __doc__; sys.exit()
val = a[1]
#num = sys.argv[2]
if str(val) not in ('s','d'): print 'not a string s (for seconds) or d (days)'; print __doc__; sys.exit()
#try: float(num)
#except ValueError: print 'not a number'; print __doc__; sys.exit()
ref = date(1970,01,01)
ref_time = time(0,0,0)
refer= datetime.datetime.combine(ref, ref_time)
print 'with respect to a reference date   ', str(refer), '\nthe provided dates are:              '
if str(val)=='d':
    for num in sys.argv:
        print str(num)
        try:
            s=float(str(num).replace(',','')) 
            out = (refer + datetime.timedelta(s)).strftime("%Y-%m-%d %H:%M:%S")
            print str(out)
        except ValueError: 
            pass
        #if str(num) not in ('s','d'):
        
        #print 'smth'
        #else:
        #    print 's or d', num
if str(val)=='s':
    for num in sys.argv:
        try:
            s=float(num) 
            out = (refer + datetime.timedelta(s/(3600*24))).strftime("%Y-%m-%d %H:%M:%S")
            print str(out)            
        except ValueError: 
            pass

