#### Files:

* [polygon_zoom.py](https://source.uit.no/mitya/pytools_git/blob/master/polygon_zoom.py) 

#### Description:

The polygon area can be picked. The rectangular mesh grid containing the polygon area is created. The range of a colobar is defined by the interior points of this polygon area.  Thus this tool can be used just for the purpose of finding out of variable range within the area of interest.


#### Usage:
 
```
python polygon_zoom.py -i /global/work/jsk/S800/norseas_800m_avg.nc_2006051212 -v temp  &
```
Left-clicks add vertices to the line - it results to a segmented line. Line can pass through masked area.

A right-click puts this process to the end and fires a window with two plots.

The colorbar range is defined by interior points of the polygon area.

### Sample outputs:

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
Thus thye next command may look like:

```
 python polygon_zoom.py -i /global/work/jsk/S800/norseas_800m_avg.nc_2006051212 -v temp  --ref_datetime 1948-01-01 00:00:00 --yrange  513:948  --xrange  338:957  --var_min  -1.66292405128  --var_max  3.79804301262 &
```
![poly_zoom](poly2.png)

![polyzoom](poly3.png)



```
the following arguments can be passed to the script for further zooming if needed:
--yrange  659:925  --xrange  345:654  --var_min  -0.852001547813  --var_max  3.5637383461
```

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

The coordinate ranges can be provided in percents with respect to grid dimensions (if unknown) with ```--xzoom``` and ```--yzoom```:

```
python polygon_zoom.py -i /global/work/jsk/S800/norseas_800m_avg.nc_2006051212 -v h --xzoom 80:95 --yzoom 5:20 --var_min 217 --var_max 533 
```