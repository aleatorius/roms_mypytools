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





f = Dataset(args.inf)



inter_list = []
constants = []

for i in f.variables.keys():
    print i, f.variables[i].dimensions
    try:
        dims = []
        if len(f.variables[i].dimensions)>0:
            for j in f.variables[i].dimensions:
                dims.append(j)

            print dims, "dims"
            inter_list.append((i,dims))
        else:
            constants.append(i)

    except:
        pass

#range_eta_rho=[100,571]
#range_xi_rho=[730,1231]
ranges = {}
#a20
dx=20000.
ranges["eta_rho"] = [20,115]
ranges["xi_rho"]=[146,247]
#a4
#dx = 4000
#ranges["eta_rho"] = [100,571]
#ranges["xi_rho"]=[730,1231]
#ranges["eta_rho"] = [0,1201]
#ranges["xi_rho"]=[0,1601]

ranges["eta_psi"] = ranges["eta_rho"][:]
ranges["xi_psi"] = ranges["xi_rho"][:]
ranges["xi_psi"][1]=ranges["xi_psi"][1]-1
ranges["eta_psi"][1]=ranges["eta_psi"][1]-1


ranges["eta_u"] = ranges["eta_rho"]
ranges["xi_u"] =ranges["xi_rho"][:]
ranges["xi_u"][1]= ranges["xi_u"][1]-1


ranges["xi_v"] = ranges["xi_rho"]
ranges["eta_v"] =ranges["eta_rho"][:]
ranges["eta_v"][1]= ranges["eta_v"][1]-1

print ranges




for i in inter_list:
    print i, i[1], "list"
    if i[0] !="hraw":
        string = "ncks -v "+ str(i[0])+" "
        for dim in i[1]:
            print dim
            string += "-d "+str(dim)+","+str(ranges[dim][0])+","+str(ranges[dim][1])+" "

        string += " "+args.inf+" -O "+str(i[0])+"_sliced.nc"
        os.system(string)
    else:
        pass
string = "ncks -v "
for i in constants:
    if i==constants[-1]:
        string += str(i)+" "
    else:
        string += str(i)+","
string+= args.inf+" -O "+"constants_sliced.nc"
print string
os.system(string)



string =str("""ncap2 -O -s 'xl=""")+str(int((ranges["xi_rho"][1]-ranges["xi_rho"][0])*dx))+"""' constants_sliced.nc -o constants_sliced.nc"""
print string
os.system(string)
string =str("""ncap2 -O -s 'el=""")+str(int((ranges["eta_rho"][1]-ranges["eta_rho"][0])*dx))+"""' constants_sliced.nc -o constants_sliced.nc"""
os.system(string)
print string
#this one depends on sliced region
string = """ncatted -O -a false_easting,grid_mapping,o,d,"1260000" constants_sliced.nc"""
os.system(string)
string = """ncatted -O -a false_northing,grid_mapping,o,d,"2170000" constants_sliced.nc"""
os.system(string)
#a4
#string = """ncatted -O -a proj4string,grid_mapping,o,c,"+proj=stere +lat_0=90 +lon_0=58 +x_0=1260000.0 +y_0=2170000.0 +lat_ts=60 +units=m +a=6.371e+06 +e=0 +no_defs" constants_sliced.nc"""
#a20
string = """ncatted -O -a proj4,grid_mapping,o,c,"+proj=stere +lat_0=90 +lon_0=58 +x_0=1260000.0 +y_0=2170000.0 +lat_ts=60 +units=m +a=6.371e+06 +e=0 +no_defs" constants_sliced.nc"""
os.system(string)


f.close()

if not args.outf:
    output = args.inf+"_region"
else:
    output = args.outf
os.system("mv h_sliced.nc "+output)
os.system("for i in *_sliced.nc; do ncks -A $i "+output+";done")
os.system("rm -f *_sliced.nc")

for i in ["eta_rho", "eta_u", "eta_v", "xi_rho","xi_u","xi_v"]:
    string = """ncap2 -O -s "("""+i+"""=double("""+i+""")-"""+str(int(ranges[i][0]*dx))+""")" """+output+""" -o """+output
    print string
    os.system(string)
