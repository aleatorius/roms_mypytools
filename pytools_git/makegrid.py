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
'-rst', 
help='input sample rst file', 
dest='rst', 
action="store"
)
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
miss = open("missing_in_rst.txt","w")



def unpack(ina):
    if ina.ndim == 0:
        print "is it scalar or 0d array?"
        outa = ina[()]
    else:
        outa = np.zeros(ina.shape)
        outa[:] = ina[:]
    return outa




#f = Dataset('/home/mitya/vilje_rivers.nc')
f = Dataset(args.inf)
g = Dataset(args.rst)


#if not args.outf:
#    nc = Dataset(args.inf+"_filtered", 'w', format='NETCDF3_CLASSIC')
#else:
#    nc = Dataset(args.outf, 'w', format='NETCDF3_CLASSIC')
#for i in f.ncattrs():
#    print i, f.getncattr(i)
#    nc.setncattr(i, f.getncattr(i))
#nc.delncattr('history')
#nc.setncattr('history', f.getncattr('history')+'\n Modified by '+str(os.path.basename(__file__))+' '+str(tm.strftime("%c")))


#for i in f.dimensions.keys():
#    print i
#    nc.createDimension(i, len(f.dimensions[i]))

inter_time = []
inter_notime = []


for i in g.variables.keys():
    print i, g.variables[i].dimensions
    try:
        print "try statement"
        print f.variables[i].dimensions
#        for j in f.variables[i].ncattrs():
#            print j, ": ", f.variables[i].getncattr(j), f.variables[i].dimensions
#            w.setncattr(j, f.variables[i].getncattr(j))
        #nc.variables[i][:]=f.variables[i]
#        arr = []
        if any("eta" in s for s in g.variables[i].dimensions):
            if any("eta_rho" in l for l in g.variables[i].dimensions):
                inter_notime.append((i,"rho"))
            elif any("eta_psi" in l for l in g.variables[i].dimensions):
                inter_notime.append((i,"psi"))
            elif any("eta_u" in l for l in g.variables[i].dimensions):
                inter_notime.append((i,"u"))
            elif any("eta_v" in l for l in g.variables[i].dimensions):
                inter_notime.append((i,"v"))
            else:
                pass
        else:
            pass
    except:
        miss.write(str(i)+" "+str(g.variables[i].dimensions)+" \n")


#for i,j in enumerate(b[1]):
#        print i,j
#        nc.variables[j][:] = b[i]
print inter_time
print inter_notime, "inter notime"
#c.close()

miss.close()
f.close()
g.close()
iniout = "iniout"
for a in inter_notime:
    print a
    i=a[0]
    print  "a_0", i
    if a[1]=="rho":
        cfg = open("template.cfg", "r")
        inp_contents = cfg.readlines()
        input_ind = inp_contents.index("[input]\n")
        output_ind =  inp_contents.index("[output]\n")
        contents = inp_contents[:]
        os.system("ncks -v "+"grid_mapping,spherical,lat_"+str(a[1])+",lon_"+str(a[1])+",mask_"+str(a[1])+",mask_"+str(a[1])+","+str(i)+" "+args.inf+" -o "+"inp_"+str(i)+".nc")
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
        cfg = open("template_u.cfg", "r")
        inp_contents = cfg.readlines()
        input_ind = inp_contents.index("[input]\n")
        output_ind =  inp_contents.index("[output]\n")
        contents = inp_contents[:]
        os.system("ncks -v "+"lat_"+str(a[1])+",lon_"+str(a[1])+",mask_"+str(a[1])+",mask_"+str(a[1])+","+str(i)+" "+args.inf+" -o "+"inp_"+str(i)+".nc")
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
        cfg = open("template_v.cfg", "r")
        inp_contents = cfg.readlines()
        input_ind = inp_contents.index("[input]\n")
        output_ind =  inp_contents.index("[output]\n")
        contents = inp_contents[:]
        os.system("ncks -v "+"lat_"+str(a[1])+",lon_"+str(a[1])+",mask_"+str(a[1])+",mask_"+str(a[1])+","+str(i)+" "+args.inf+" -o "+"inp_"+str(i)+".nc")
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
        


#to merge into one file
#mitya@service0:/work/mitya/interp_a20_a4> mv iniout_zeta.nc output.nc 
#mitya@service0:/work/mitya/interp_a20_a4> f=output.nc 
#mitya@service0:/work/mitya/interp_a20_a4> for i in iniout_*; do ncks -A $i $f;done    
