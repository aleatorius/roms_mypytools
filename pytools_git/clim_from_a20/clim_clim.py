#!/home/mitya/testenv/bin/python -B                                            # -*- coding: utf-8 -*-                                     
import os
import sys
from datetime import datetime

import numpy as np
from netCDF4 import Dataset

import netcdftime
import time as tm
from calendar import monthrange
import datetime 
from datetime import date, time
import argparse
# load boost before: module load boost/1.53.0 nco

parser = argparse.ArgumentParser(description='transect write 0.1')

parser.add_argument(
'-i', 
help='input file', 
dest='inf', 
action="store"
)
parser.add_argument(
'-clim', 
help='input file', 
dest='clim', 
action="store"
)

parser.add_argument(
'-o', 
help='input file', 
dest='outf', 
action="store"
)


args = parser.parse_args()




def unpack(ina):
    if ina.ndim == 0:
        print "is it scalar or 0d array?"
        outa = ina[()]
    else:
        outa = np.zeros(ina.shape)
        outa[:] = ina[:]
    return outa





f = Dataset(args.clim)
g = Dataset(args.inf)



inter_list = []
constants = []

for i in f.variables.keys():
    print i, f.variables[i].dimensions
    if i == "clim_time":
        inter_list.append("ocean_time")
    else:
        try:
            if len(g.variables[i].dimensions)>0:
                inter_list.append(str(i))
            else:
                constants.append(str(i))
        except:
            pass
print inter_list
string = "ncks -v "
for i,j in enumerate(inter_list):
    print i,j
    if i!=len(inter_list)-1:
        if j not in ["x", "y"]:
            string += str(j)+","
        else:
            pass
    else:
        string += str(j)+" "

if not args.outf:
    output = args.inf+"_filtered"
else:
    output = args.outf

string += args.inf+" -O "+output
print string
os.system(string)
print constants
sys.exit()
        

if len(constants)!=0:
    string = "ncks -v "
    for i in constants:
        if i==constants[-1]:
            string += str(i)+" "
        else:
            string += str(i)+","
    string+= args.inf+" -O "+"constants_sliced.nc"
    print string
else:
    pass


f.close()


os.system("mv zeta_sliced.nc "+output)
os.system("for i in *_sliced.nc; do echo $i;  ncks -A $i "+output+";done")
os.system("rm -f *_sliced.nc")

