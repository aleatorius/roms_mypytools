#!/global/apps/python/2.7.3/bin/python
# rewrite m-script to python script
# Yoshie, Dmitry, 2015.04.25
#% pick up modell data from one grid point (time series)
#% files listed in a list (e.g. 2008_norfjords_160m_his_list.txt) are read
#% grid point provided as ind = [x,y];                                                            
import os
import glob
from netCDF4 import Dataset
import numpy as np
listing=[]
#mn = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
#yr=["2006","2007","2008","2009"]
mn = ["02","03"]
yr=["2006"]

# Position #1 i:y-direction, j:x-direction
grdp = (372,34)
print "grid point (i,j)"
print grdp


for year in yr:
    for month in mn:
        string1 = "norfjords_160m_his.nc_"+str(year)+str(month)+"*"
        for root,dirs,files in os.walk('/global/work/jsk/K160'):
            listing = glob.glob(os.path.join(root,string1))
            print listing
            time_rec = 0
            filename = "kf_"+str(year)+str(month)+".nc"
            ts = Dataset(filename, mode='w',format='NETCDF3_CLASSIC')
            print  
            print(ts)

            s_rho_dim = ts.createDimension('s_rho', 35)   
            station_dim = ts.createDimension('station', 1)   
            time_dim = ts.createDimension('ocean_time', None) # unlimited axis (can be appended to).
            for dim in ts.dimensions.items():
                print(dim)

            ts.setncattr("title","time series for stations points")


            Ipos = ts.createVariable('Ipos', np.float64, ('station',))
            Ipos.long_name = "stations I-direction positions"
            Jpos = ts.createVariable('Jpos', np.float64, ('station',))
            Jpos.long_name = "stations J-direction positions"
            time_var = ts.createVariable('ocean_time', np.float64, ('ocean_time',))
            time_var.units = "seconds since 1948-01-01 00:00:00"
            time_var.long_name = 'ocean_time'
            time_var.calendar = "gregorian" ;
            time_var.field = "time, scalar, series" ;

            Ipos[:] = np.array(grdp[0])
            Jpos[:] = np.array(grdp[1])

            u =  ts.createVariable('u', np.float32, ('ocean_time','station','s_rho',))
            v =  ts.createVariable('v', np.float32, ('ocean_time','station','s_rho',))
            ubar =  ts.createVariable('ubar', np.float32, ('ocean_time','station','s_rho',))
            vbar =  ts.createVariable('vbar', np.float32, ('ocean_time','station','s_rho',))
            temp =  ts.createVariable('temp', np.float32, ('ocean_time','station','s_rho',))
            salt =  ts.createVariable('salt', np.float32, ('ocean_time','station','s_rho',))
            zeta =  ts.createVariable('zeta', np.float32, ('ocean_time','station',))
            aice =  ts.createVariable('aice', np.float32, ('ocean_time','station',))
            hice =  ts.createVariable('hice', np.float32, ('ocean_time','station',))
            Uwind =  ts.createVariable('Uwind', np.float32, ('ocean_time','station',))
            Vwind =  ts.createVariable('Vwind', np.float32, ('ocean_time','station',))
            swrad =  ts.createVariable('swrad', np.float32, ('ocean_time','station',))


            #print u.shape
            u.long_name = "u-momentum component" 
            u.units = "meter second-1" 
            u.time = "ocean_time" 
            u.field = "u-velocity, scalar, series" 

            v.long_name = "v-momentum component" 
            v.units = "meter second-1" 
            v.time = "ocean_time" 
            v.field = "v-velocity, scalar, series" 

            ubar.long_name = "vertically integrated u-momentum component" 
            ubar.units = "meter second-1" 
            ubar.time = "ocean_time" 
            ubar.field = "ubar-velocity, scalar, series" 

            vbar.long_name = "vertically integrated v-momentum component" 
            vbar.units = "meter second-1" 
            vbar.time = "ocean_time" 
            vbar.field = "vbar-velocity, scalar, series" 

            temp.long_name = "potential temperaturet" 
            temp.units = "Celsius" 
            temp.time = "ocean_time" 
            temp.field = "temperature, scalar, series" 

            salt.long_name = "salinity" 
            salt.units = "" 
            salt.time = "ocean_time" 
            salt.field = "salinity, scalar, series" 

            Uwind.long_name = "surface u-wind component" 
            Uwind.units = "meter second-1" 
            Uwind.time = "ocean_time" 
            Uwind.field = "u-wind, scalar, series" 

            Vwind.long_name = "surface v-wind component" 
            Vwind.units = "meter second-1" 
            Vwind.time = "ocean_time" 
            Vwind.field = "v-wind, scalar, series" 

            zeta.long_name = "free-surface" 
            zeta.units = "meter" 
            zeta.time = "ocean_time" 
            zeta.field = "free-surface, scalar, series" 

            swrad.long_name = "solar shortwave radiation flux" 
            swrad.units = "watt meter-2" 
            swrad.time = "ocean_time" 
            swrad.field = "shortwave radiation, scalar, series" 

            aice.long_name = "fraction of cell coverd by ice" 
            aice.units = " " 
            aice.time = "ocean_time" 
            aice.field = "ice concentration, scalar, series" 

            hice.long_name = "average ice thickness in cell" 
            hice.units = " " 
            hice.time = "ocean_time" 
            hice.field = "ice thickness, scalar, series" 

            for item in sorted(listing):
                print item

                f = Dataset(item)

                for counter,t in enumerate(f.variables["ocean_time"][:]):
                    print counter, t
                    print grdp[0], grdp[1]
                    print f.variables["u"][counter,:,grdp[0],grdp[1]].shape, u.shape
                    temp[time_rec,:]=f.variables["temp"][counter,:,grdp[0],grdp[1]]
                    salt[time_rec,:]=f.variables["salt"][counter,:,grdp[0],grdp[1]]
                    print f.variables["zeta"][:].shape
                    zeta[time_rec]=f.variables["zeta"][counter,grdp[0],grdp[1]]
                    aice[time_rec]=f.variables["aice"][counter,grdp[0],grdp[1]]
                    hice[time_rec]=f.variables["hice"][counter,grdp[0],grdp[1]]
                    Uwind[time_rec]=f.variables["Uwind"][counter,grdp[0],grdp[1]]
                    Vwind[time_rec]=f.variables["Vwind"][counter,grdp[0],grdp[1]]
                    swrad[time_rec]=f.variables["swrad"][counter,grdp[0]-1,grdp[1]]
                    u1 =f.variables["u"][counter,:,grdp[0]-1,grdp[1]]
                    u2 =f.variables["u"][counter,:,grdp[0],grdp[1]]
                    v1 =f.variables["v"][counter,:,grdp[0],grdp[1]-1]
                    v2 =f.variables["v"][counter,:,grdp[0],grdp[1]]
                    u[time_rec,:]=(u1+u2)/2.
                    v[time_rec,:]=(v1+v2)/2.
                    print u.shape
                    time_var[time_rec] = t
                    time_rec+=1
                    print time_rec, counter

                f.close()

            ts.close()



print u.shape
ts.close()


