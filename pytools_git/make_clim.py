#!/home/mitya/testenv/bin/python -B                                            # -*- coding: utf-8 -*-                                     
import os
import sys
import glob
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




def unpack(ina):
    if ina.ndim == 0:
        print "is it scalar or 0d array?"
        outa = ina[()]
    else:
        outa = np.zeros(ina.shape)
        outa[:] = ina[:]
    return outa

outdir="/global/work/mitya/temp/"

climdir = "/global/work/mitya/Clim/"
myocean = "/global/work/mitya/metno/MyOcean/"
#years = ["2000","2001","2002"]
years = ["2002"]
bio = ["NO3", "PHYC"]

for year in years:
    print year
    
#    for climfile in sorted(glob.glob(climdir+"ocean_*"+year+"*")):
#        print climfile
#        string = "ncks -O -v zeta "+climfile+ " "+ outdir+year + "_zeta.nc"
#        os.system(string)
#        for i in range(0,12):
#            if i in range(0,9):
#                print i
#                string = "ncks -O -d clim_time,"+str(i)+ " "+ outdir+year + "_zeta.nc "+ \
#                    outdir+ "zeta_"+year+"_0"+str(i+1)+".nc"
#            else:
#                string = "ncks -O -d clim_time,"+str(i)+ " "+ outdir+year + "_zeta.nc "+ \
#                    outdir+ "zeta_"+year+"_"+str(i+1)+".nc"
#            print string
 #           os.system(string)
    for biocomp in bio:
        print biocomp, year
        biolist = sorted(glob.glob(myocean+year+"/*"+year+"*"+biocomp+"*"))
        for item in biolist:
            print item.split("/")
            cfg = open("fimex_config/template.cfg", "r")
            inp_contents = cfg.readlines()
            input_ind = inp_contents.index("[input]\n")
            output_ind =  inp_contents.index("[output]\n")
            contents = inp_contents[:]
            contents.insert(input_ind+1, "file="+item+"\n")
            contents.insert(output_ind+2, "file="+outdir+item.split("/")[-1]+"_inter\n")
            cfg_out = open("list.cfg", "w")
            contents = "".join(contents)
            cfg_out.write(contents)
            cfg_out.close()
            os.system("fimex -c list.cfg")
