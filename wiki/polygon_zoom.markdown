#### Files:

* [polygon_zoom.py](https://github.com/aleatorius/roms_mypytools/blob/master/pytools_git/polygon_zoom.py)  
* [polygon_zoom_int.py](https://github.com/aleatorius/roms_mypytools/blob/master/pytools_git/polygon_zoom_int.py) 

#### Description:

A polygonal area can be picked. The rectangular mesh grid containing this polygon area is created. The range of the colobar is defined by the interior points of the polygonal area.  Thus this tool can be used for the purpose of finding the range of variable in the the area of interest.


#### Usage:
 
* [polygon_zoom.py](https://github.com/aleatorius/roms_mypytools/blob/master/pytools_git/polygon_zoom.py) 

```
python polygon_zoom.py -i /global/work/jsk/S800/norseas_800m_avg.nc_2006051212 -v temp  &
```
Left-clicks add vertices to the line - it results to a segmented line. Line can pass through masked area.

A right-click puts this process to the end and fires a window with two plots.

The colorbar range is defined by interior points of the polygon area.

```
python polygon_zoom.py -i /global/work/jsk/S800/norseas_800m_avg.nc_2006051212 -v temp --pout foo
```
Here it writes out txt-files for each polygon, a writing is activated by prefix ```-pout```, and files ```foo_0, foo_1, foo_2,...``` are created.

```
python polygon_zoom.py -i /global/work/jsk/S800/norseas_800m_avg.nc_2006051212 -v temp --ref_datetime 1948-01-01 00:00:00 --pin foo_1 &
```
In this way the script reads from a previously created txt file```foo_1``` the vertices of a polygon and shows a plot, which is not interactive.

* [polygon_zoom_int.py](https://github.com/aleatorius/roms_mypytools/blob/master/pytools_git/polygon_zoom_int.py) 

This tool deals with vertically integrated variable (thus it should have vertical dimension). Mesh plot presents integrated variable on the grid. In usage this script is almost identical to [polygon_zoom_read.py](https://github.com/aleatorius/roms_mypytools/blob/master/pytools_git/polygon_zoom_read.py).  
Also it prints in the title the "mass" of variable in the area (whole area or polygonal part of it). This value should be scaled afterwards accordingly to horizontal resolution. In the script it is calculating taking a cell area as a dimensionless unit. 
```
python polygon_zoom_int.py -i /global/work/mitya/run/Arctic-20km/ocean_rst_20051212.nc -v phytoplankton  --pout s &
```
### Sample outputs and usages:

```
python polygon_zoom.py -i /global/work/jsk/S800/norseas_800m_avg.nc_2006051212 -v temp
```

![poly_zoom](poly0.png)

![polyzoom](poly1.png)

NB: The date can be corrected via prefix ```--ref_datetime 1948-01-01 00:00:00``` (it is format sensitive!). The default reference date is ```1970-01-01 00:00:00``` 

```
python polygon_zoom.py -i /global/work/jsk/S800/norseas_800m_avg.nc_2006051212 -v temp  --ref_datetime 1948-01-01 00:00:00 &
```

It is possible to zoom further on, the suggested ranges for variable and grid are printed in the terminal:
```
the following arguments can be passed to the script for further zooming if needed:
--yrange  513:948  --xrange  338:957  --var_min  -1.66292405128  --var_max  3.79804301262
```
Thus a command may look like:

```
 python polygon_zoom.py -i /global/work/jsk/S800/norseas_800m_avg.nc_2006051212 -v temp  --ref_datetime 1948-01-01 00:00:00 --yrange  513:948  --xrange  338:957  --var_min  -1.66292405128  --var_max  3.79804301262 &
```
![poly_zoom](poly2.png)

![polyzoom](poly3.png)



```
the following arguments can be passed to the script for further zooming if needed:
--yrange  659:925  --xrange  345:654  --var_min  -0.852001547813  --var_max  3.5637383461
```

A different s-layer can be specified with prefix ```--vert```  (the default is ````34``` - which is the surface layer. In the examples I consider here there are 35 vertical sigma layers):

```
python polygon_zoom.py -i /global/work/jsk/S800/norseas_800m_avg.nc_2006051212 -v temp --ref_datetime 1948-01-01 00:00:00 --yrange  659:925  --xrange  345:654  --var_min  -0.852001547813  --var_max  3.5637383461   --vert 0 &
```
![poly_zoom](poly8.png)

A different variable can be passed to the script, e.g. bathymetry ```-v h``` (NB: don't forget to modify or delete variable ranges defined by ``` --var_min  -0.852001547813  --var_max  3.5637383461``` ):

```
python polygon_zoom.py -i /global/work/jsk/S800/norseas_800m_avg.nc_2006051212 -v h --ref_datetime 1948-01-01 00:00:00 --yrange  659:925  --xrange  345:654   &
```


![poly_zoom](poly5.png)

![polyzoom](poly6.png)

```
the following arguments can be passed to the script for further zooming if needed:
--yrange  739:920  --xrange  349:604  --var_min  1530.90808784  --var_max  4541.1597306
```

![poly_zoom](poly7.png)

The coordinate ranges can be provided in percents with respect to grid dimensions (if unknown to user) with ```--xzoom``` and ```--yzoom```:

```
python polygon_zoom.py -i /global/work/jsk/S800/norseas_800m_avg.nc_2006051212 -v h --xzoom 80:95 --yzoom 5:20 --var_min 217 --var_max 533 
```
Usage of [polygon_zoom_int.py](https://github.com/aleatorius/roms_mypytools/blob/master/pytools_git/polygon_zoom_int.py):

```
python polygon_zoom_int.py -i /global/work/mitya/run/Arctic-20km/archive_2005_cortemp/ocean_avg_2006_06_20_0052.nc -v phytoplankton  --pout s  &
```

![poly_zoom](phyt_zoom0.png)

singular values on the west boundary can be zoomed out:

![poly_zoom](phyt_zoom1.png)


#### Masking:

It is possible to turn on the mask with prefix ```--mask yes``` (it will work if there is a variable called ```mask_rho```) - it is useful for variables which land values are not filled with  ```1e+37```

![poly_zoom](mask0.png)

```
python polygon_zoom.py -i /global/work/jsk/S800/norseas_800m_avg.nc_2005090112 -v h --yrange  461:602  --xrange  339:583  --var_min  10.0  --var_max  2062.53437468 --mask yes

```

![poly_zoom](mask1.png)

#### Options

The list of all options can be requested with ```-h``` prefix:
```
[mitya@stallo-2 pytools_git]$ python polygon_zoom.py -h

usage: polygon_zoom_read.py [-h] [--ref_datetime REF_DATETIME REF_DATETIME]
                            [--contourf {yes,no}] [-i INF] [--pout POUT]
                            [--pin PIN] [-v VARIABLE] [--f {s,d}]
                            [--time_rec TIME_REC] [--time TIME] [--vert VERT]
                            [--xzoom XZOOM] [--yzoom YZOOM] [--xrange XRANGE]
                            [--yrange YRANGE] [--var_min VAR_MIN]
                            [--var_max VAR_MAX]

polygon zoom

optional arguments:
  -h, --help            show this help message and exit
  --ref_datetime REF_DATETIME REF_DATETIME
                        reference date time: 1970-01-01 00:00:00
  --contourf {yes,no}   colormesh or contourf
  -i INF                input file
  --pout POUT           output polygon file
  --pin PIN             input polygon file
  -v VARIABLE           variable
  --f {s,d}             time format - seconds or days with respect to reference date and time
  --time_rec TIME_REC   time records name - ocean_time, clim_time, time, etc
  --time TIME           time counter
  --vert VERT           vertical coordinate number
  --xzoom XZOOM         zoom along x direction, range is defined in percents
  --yzoom YZOOM         zoom along y direction, range is defined in percents
  --xrange XRANGE       zoom along x direction
  --yrange YRANGE       zoom along y direction
  --var_min VAR_MIN     minimum value of variable
  --var_max VAR_MAX     max value of variable

```
