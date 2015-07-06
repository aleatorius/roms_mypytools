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


fimexdir="/home/mitya/pytools_git/fimex_config/"

#f = Dataset('/home/mitya/vilje_rivers.nc')
f = Dataset(args.inf)



inter_time = []
inter_notime = []


for i in f.variables.keys():
    print i, f.variables[i].dimensions
    try:
        print "try statement"
    #    print f.variables[i].dimensions
#        for j in f.variables[i].ncattrs():
#            print j, ": ", f.variables[i].getncattr(j), f.variables[i].dimensions
#            w.setncattr(j, f.variables[i].getncattr(j))
        #nc.variables[i][:]=f.variables[i]
#        arr = []
        if any("eta" in s for s in f.variables[i].dimensions):
            if any("time" in l for l in f.variables[i].dimensions):
                if any("eta_rho" in l for l in f.variables[i].dimensions):
                    inter_time.append((i,"rho"))
                elif any("eta_psi" in l for l in f.variables[i].dimensions):
                    inter_time.append((i,"psi"))
                elif any("eta_u" in l for l in f.variables[i].dimensions):
                    inter_time.append((i,"u"))
                elif any("eta_v" in l for l in f.variables[i].dimensions):
                    inter_time.append((i,"v"))
                else:
                    pass
            else:
                inter_notime.append(i)
        else:
            pass
    except:
        pass


#for i,j in enumerate(b[1]):
#        print i,j
#        nc.variables[j][:] = b[i]
print "time dependent", inter_time
print "time independent", inter_notime

f.close()

iniout = "iniout"
for a in inter_time:
    print a
    i=a[0]
    if a[1]=="rho":
        cfg = open(fimexdir+"template.cfg", "r")
        inp_contents = cfg.readlines()
        input_ind = inp_contents.index("[input]\n")
        output_ind =  inp_contents.index("[output]\n")
        contents = inp_contents[:]
        os.system("ncks -v "+"lat_"+str(a[1])+",lon_"+str(a[1])+","+str(i)+" "+args.inf+" -o "+"inp_"+str(i)+".nc")
        contents.insert(input_ind+1, "file=inp_"+str(i)+".nc\n")
        contents.insert(output_ind+2, "file="+str(iniout)+"_"+str(i)+".nc\n")
        cfg_out = open("list.cfg", "w")
        contents = "".join(contents)
        cfg_out.write(contents)
        cfg_out.close()
        os.system("fimex -c list.cfg")
        ncrename = "ncrename -v lat,lat_"+str(a[1])+" -v lon,lon_"+str(a[1])+" "+str(iniout)+"_"+str(i)+".nc" 
        print ncrename
        os.system(ncrename)

        cfg.close()
    elif a[1]=="u":
        cfg = open(fimexdir+"template_u.cfg", "r")
        inp_contents = cfg.readlines()
        input_ind = inp_contents.index("[input]\n")
        output_ind =  inp_contents.index("[output]\n")
        contents = inp_contents[:]
        os.system("ncks -v "+"lat_"+str(a[1])+",lon_"+str(a[1])+","+str(i)+" "+args.inf+" -o "+"inp_"+str(i)+".nc")
        contents.insert(input_ind+1, "file=inp_"+str(i)+".nc\n")
        contents.insert(output_ind+2, "file="+str(iniout)+"_"+str(i)+".nc\n")
        cfg_out = open("list.cfg", "w")
        contents = "".join(contents)
        cfg_out.write(contents)
        cfg_out.close()
        os.system("fimex -c list.cfg")
        ncrename = "ncrename -v lat,lat_"+str(a[1])+" -v lon,lon_"+str(a[1])+" "+str(iniout)+"_"+str(i)+".nc" 
        print ncrename
        os.system(ncrename)
        cfg.close()
    elif a[1]=="v":
        cfg = open(fimexdir+"template_v.cfg", "r")
        inp_contents = cfg.readlines()
        input_ind = inp_contents.index("[input]\n")
        output_ind =  inp_contents.index("[output]\n")
        contents = inp_contents[:]
        os.system("ncks -v "+"lat_"+str(a[1])+",lon_"+str(a[1])+","+str(i)+" "+args.inf+" -o "+"inp_"+str(i)+".nc")
        contents.insert(input_ind+1, "file=inp_"+str(i)+".nc\n")
        contents.insert(output_ind+2, "file="+str(iniout)+"_"+str(i)+".nc\n")
        cfg_out = open("list.cfg", "w")
        contents = "".join(contents)
        cfg_out.write(contents)
        cfg_out.close()
        os.system("fimex -c list.cfg")
        ncrename = "ncrename -v lat,lat_"+str(a[1])+" -v lon,lon_"+str(a[1])+" "+str(iniout)+"_"+str(i)+".nc"
        print ncrename
        os.system(ncrename)
        cfg.close()
    else:
        pass
        

if not args.outf:
    output = args.inf+"_hinter"
else:
    output = args.outf
os.system("rm -f inp_*.nc")
os.system(" nccopy -k 2 iniout_zeta.nc "+output)
os.system("rm -f iniout_zeta.nc")
os.system("for i in iniout_*.nc; do echo $i;  ncks -A $i "+output+";done")
os.system("rm -f iniout_*.nc")

#to merge into one file
#mitya@service0:/work/mitya/interp_a20_a4> mv iniout_zeta.nc output.nc 
#mitya@service0:/work/mitya/interp_a20_a4> f=output.nc 
#mitya@service0:/work/mitya/interp_a20_a4> for i in iniout_*; do ncks -A $i $f;done    
