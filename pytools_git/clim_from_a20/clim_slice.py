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

ranges["eta_rho"] = [20,115]
ranges["xi_rho"]=[146,247]
#ranges["eta_rho"] = [19,114]
#ranges["xi_rho"]=[145,246]
#ranges["eta_rho"] = [100,571]
#ranges["xi_rho"]=[730,1231]

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
    print i[0]
    if i[0] not in ["lon_rho", "lat_rho"]:
        if i[0] not in ["x", "y"]:
            string = "ncks -v "+ str(i[0])+" "
            for dim in i[1]:
                if dim not in ["ocean_time","clim_time","s_rho"]:
                    string += "-d "+str(dim)+","+str(ranges[dim][0])+","+str(ranges[dim][1])+" "
                else:
                    pass

            string += " "+args.inf+" -O "+str(i[0])+"_sliced.nc"
            print string
            os.system(string)
        else:
            pass

    else:
        print "lotlon", i[0]
        dimensions=["eta_rho", "xi_rho"]
        string = "ncks -v "+ str(i[0])+" "
        for dim in dimensions:
            string += "-d "+str(dim)+","+str(ranges[dim][0])+","+str(ranges[dim][1])+" "
            

        string += " "+args.inf+" -O "+str(i[0])+"_sliced.nc"
        print string
        os.system(string)
        

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

if not args.outf:
    output = args.inf+"_region"
else:
    output = args.outf
os.system("mv zeta_sliced.nc "+output)
os.system("for i in *_sliced.nc; do echo $i;  ncks -A $i "+output+";done")
os.system("rm -f *_sliced.nc")

