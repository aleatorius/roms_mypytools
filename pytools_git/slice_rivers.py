#!/home/mitya/testenv/bin/python -B                                                                                   
import os
import sys
from datetime import datetime
#import pyproj
#from pyproj import Proj
import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import *
from numpy import *
import netcdftime
import time as tm
from calendar import monthrange
import datetime 
from datetime import date, time
import argparse
parser = argparse.ArgumentParser(description='transect write 0.1')

parser.add_argument(
'-i', 
help='input file', 
dest='inf', 
action="store"
)
parser.add_argument(
'-o', 
help='output file', 
dest='outf', 
action="store"
)
parser.add_argument(
'-river', 
help='modification parameters', 
dest='river', 
action="store", 
nargs=5
)
parser.add_argument(
'-delriver', 
help='delete river with id number', 
dest='delriver', 
action="store",
default=None,
nargs=1
)


args = parser.parse_args()

print args.river 
def unpack(ina):
    if ina.ndim == 0:
        print "is it scalar or 0d array?"
        outa = ina[()]
    else:
        outa = np.zeros(ina.shape)
        outa[:] = ina[:]
    return outa


#grid_file = '/home/mitya/models/NorROMS/Apps/Common/Grid/arctic4km_grd.nc'
#grid = Dataset(grid_file)
#mask = unpack(grid.variables['mask_rho'])
#grid.close()

#f = Dataset('/home/mitya/vilje_rivers.nc')
f = Dataset(args.inf)
x_pos = f.variables["river_Xposition"][:]
e_pos = f.variables["river_Eposition"][:]
river = f.variables["river"][:]


range_eta_rho=[100,571]
range_xi_rho=[730,1231]
discard=[]
keep = []
for num,x in enumerate(x_pos):
    print num, x
    if  range_xi_rho[0] <= int(x) <= range_xi_rho[1]:
        print int(x), range_xi_rho
        if  range_eta_rho[0] <= int(e_pos[num]) <= range_eta_rho[1]:
            print int(e_pos[num]), range_eta_rho
            keep.append(river[num])
        else:
            discard.append(river[num])
    else:
        discard.append(river[num])
print keep, "keep"
print discard, "discard"


for num, river in enumerate(discard):
    print num, river
    if num == 0:
        string = "./correct_rivers.py -i "+args.inf+" -o "+args.inf+"_del -delriver "+str(int(river))
    else:
        string = "./correct_rivers.py -i "+args.inf+"_del -o "+args.inf+"_del -delriver "+str(int(river))
    print string
    os.system(string)

string =str("""ncap2 -O -s 'river_Xposition=double(river_Xposition)-""")+str(int((range_xi_rho[0])))+"' "+args.inf +" -o "+args.inf+"_shifted"
print string
os.system(string)
string =str("""ncap2 -O -s 'river_Eposition=double(river_Eposition)-""")+str(int((range_eta_rho[0])))+"' "+args.inf +"_shifted -o "+args.inf+"_shifted"
print string
os.system(string)



sys.exit()


def extract_arrays(f):
    var_array = []
    var_name = []
    for i in f.variables.keys():
        print i
        var_name.append(i)
        var_array.append(unpack(f.variables[i]))
    return var_array, var_name
        




#original data
b = extract_arrays(f) 

if args.river:
    #changed data
    epos_record = None
    xpos_record = None
    direction_record = None
    transport_record = None
    river_record = None
    for i,j in enumerate(b[1]):
        print i,j, b[0][i].shape
        if j=='river':
             for m,n in enumerate(b[0][i]):
                 if int(n)==int(args.river[0]):
                    print m,n
                    river_record=m
                 else:
                     pass
             break
    print river_record

    for i,j in enumerate(b[1]):
        if j=='river_Xposition':
            xpos_record = i
            break
        else:
            pass

    for i,j in enumerate(b[1]):
        if j=='river_Eposition':
            epos_record = i
            break
        else:
            pass

    for i,j in enumerate(b[1]):
        if j=='river_direction':
            direction_record = i
            break
        else:
            pass

    for i,j in enumerate(b[1]):
        if j=='river_transport':
            transport_record = i
            break
        else:
            pass

    print epos_record, xpos_record, direction_record, transport_record
    print b[0][epos_record][river_record]
    print b[0][xpos_record][river_record]
    print b[0][direction_record][river_record]
    print np.sum(b[0][transport_record][:,river_record])


    # making "rho points" - cells where the river flows in. 
    if np.sum(b[0][transport_record][:,river_record])>0:
        print "no mod"
    else:
        if int(b[0][direction_record][river_record])==0:
            b[0][xpos_record][river_record] = b[0][xpos_record][river_record]-1
        else:
            b[0][epos_record][river_record] = b[0][epos_record][river_record]-1

    # adjusting to a new position

    if river_record != None:
        for i,j in enumerate(b[1]):
            if j=='river_Xposition':
                print b[0][i][river_record], "xpos"
                print int(args.river[1])
                if int(args.river[4])> 0:
                    b[0][i][river_record]=int(b[0][i][river_record])+int(args.river[1])
                else:
                    if int(args.river[3])==0:
                        print "case dir 0"
                        b[0][i][river_record]=int(b[0][i][river_record]+int(args.river[1]))+1
                    else:
                        print "case 1"
                        b[0][i][river_record]=int(b[0][i][river_record])+int(args.river[1])
                print b[0][i][river_record], "xpos"
    #        print b[1][i],": \n", b[0][i]
                break
        for i,j in enumerate(b[1]):
            if j=='river_Eposition':
                print b[0][i][river_record], "epos"
                print int(args.river[2])
                if int(args.river[4])> 0:
                    b[0][i][river_record]=int(b[0][i][river_record]+int(args.river[2]))
                else:
                    if int(args.river[3])==1:
                        b[0][i][river_record]=int(b[0][i][river_record])+int(args.river[2])+1
                    else:
                        b[0][i][river_record]=int(b[0][i][river_record])+int(args.river[2])
                print b[0][i][river_record], "epos"
                break
        for i,j in enumerate(b[1]):
            if j=='river_direction':
                print i,j
                print b[0][i][river_record], "direction"
                print int(args.river[3])
                b[0][i][river_record]=int(args.river[3])
                print b[0][i][river_record], "direction"
                break
        for i,j in enumerate(b[1]):
            if j=='river_transport':
                print i,j
                print b[0][i][:,river_record], "transport"
                print int(args.river[4])
                sign=np.sign(b[0][i][:,river_record])
                b[0][i][:,river_record]=np.sign(float(args.river[4]))*(b[0][i][:,river_record]*sign)
                print b[0][i][:,river_record], "transport after"
                break
    else:
        pass




    if not args.outf:
        nc = Dataset(args.inf+"_corrected", 'w', format='NETCDF3_CLASSIC')
    else:
        nc = Dataset(args.outf, 'w', format='NETCDF3_CLASSIC')
    for i in f.ncattrs():
        print i, f.getncattr(i)
        nc.setncattr(i, f.getncattr(i))
    nc.delncattr('history')
    nc.setncattr('history', f.getncattr('history')+'\n Modified by '+str(os.path.basename(__file__))+' '+str(tm.strftime("%c")))


    for i in f.dimensions.keys():
        print i
        nc.createDimension(i, len(f.dimensions[i]))

    for i in f.variables.keys():
        print i, f.variables[i].dimensions
        w = nc.createVariable(i, 'f8',  f.variables[i].dimensions)

        for j in f.variables[i].ncattrs():
       #     print j, ": ", f.variables[i].getncattr(j), f.variables[i].dimensions
            w.setncattr(j, f.variables[i].getncattr(j))

    # assigning updated values to variables

    for i,j in enumerate(b[1]):
    #    print i,j
        nc.variables[j][:] = b[0][i]

    nc.close()

elif args.delriver:
    print "del"
    river_record = None
    for i,j in enumerate(b[1]):
        print i,j, b[0][i].shape
        if j=='river':
             for m,n in enumerate(b[0][i]):
                 if int(n)==int(args.delriver[0]):
                    print m,n
                    river_record=m
                 else:
                     pass
             break
    print river_record


    if not args.outf:
        nc = Dataset(args.inf+"_corrected", 'w', format='NETCDF3_CLASSIC')
    else:
        nc = Dataset(args.outf, 'w', format='NETCDF3_CLASSIC')
    for i in f.ncattrs():
        print i, f.getncattr(i)
        nc.setncattr(i, f.getncattr(i))
    nc.delncattr('history')
    nc.setncattr('history', f.getncattr('history')+'\n Modified by '+str(os.path.basename(__file__))+' '+str(tm.strftime("%c")))


    for i in f.dimensions.keys():
        print i
        if i == 'river':
            nc.createDimension(i, len(f.dimensions[i])-1)
        else:
            nc.createDimension(i, len(f.dimensions[i]))
       
    b_updated = []
    for i in f.variables.keys():
        print i, f.variables[i].dimensions
        if 'river' in f.variables[i].dimensions:
            print "contains river dimension"
            for k,m in enumerate(b[1]):
                if m==i:
                    position = k
                    print position, m,i
                    break
                else:
                    pass
            shape = np.array(b[0][position]).shape
            index= np.zeros(len(shape))
            index[:]=shape[:]
            index[-1]= index[-1]-1
            if len(index)==1:
                b_out = np.ones(index)
                b_out[:river_record]=b[0][position][:river_record]
                b_out[river_record:]=b[0][position][river_record+1:]
            elif len(index)==2:
                b_out = np.ones(index)
                b_out[:,:river_record]=b[0][position][:,:river_record]
                b_out[:,river_record:]=b[0][position][:,river_record+1:]
            elif len(index)==3:
                b_out = np.ones(index)
                b_out[:,:,:river_record]=b[0][position][:,:,:river_record]
                b_out[:,:,river_record:]=b[0][position][:,:,river_record+1:]
            else:
                pass
        else:
            for k,m in enumerate(b[1]):
                if m==i:
                    position = k
                    print position, m,i
                    break
                else:
                    pass
            b_out = b[0][position]
        b_updated.append(b_out)

        w = nc.createVariable(i, 'f8',  f.variables[i].dimensions)
        print  f.variables[i].dimensions

        for j in f.variables[i].ncattrs():
       #     print j, ": ", f.variables[i].getncattr(j), f.variables[i].dimensions
            w.setncattr(j, f.variables[i].getncattr(j))
    
    for i,j in enumerate(b[1]):
    #    print i,j
        print j, b_updated[i].shape, b[0][i].shape
        nc.variables[j][:] = b_updated[i]
    nc.close()
else:
    pass

f.close()
