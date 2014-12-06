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

NB: the date can be corrected via prefix ```--ref_datetime 1948-01-01 00:00:00``` (it is format sensitive!):

```
python polygon_zoom.py -i /global/work/jsk/S800/norseas_800m_avg.nc_2006051212 -v temp  --ref_datetime 1948-01-01 00:00:00 &
```

The default reference date is ```1970-01-01 00:00:00``` 

It is possible to zoom further on, the suggested ranges are printed in terminal:
```
the following arguments can be passed to the script for further zooming if needed:
--yrange  513:948  --xrange  338:957  --var_min  -1.66292405128  --var_max  3.79804301262
```

```
 python polygon_zoom.py -i /global/work/jsk/S800/norseas_800m_avg.nc_2006051212 -v temp  --ref_datetime 1948-01-01 00:00:00 --yrange  513:948  --xrange  338:957  --var_min  -1.66292405128  --var_max  3.79804301262 &

```
```
the following arguments can be passed to the script for further zooming if needed:
--yrange  659:925  --xrange  345:654  --var_min  -0.852001547813  --var_max  3.5637383461

[mitya@stallo-1 pytools_git]$ python polygon_zoom.py -i /global/work/jsk/S800/norseas_800m_avg.nc_2006051212 -v temp  --ref_datetime 1948-01-01 00:00:00 --yrange  659:925  --xrange  345:654  --var_min  -0.852001547813  --var_max  3.5637383461 &
```



Bathymetry zoom (impose masking?):

![poly_zoom](poly2.png)

![polyzoom](poly3.png)

It is possible to zoom further on, in the following way:

```
python polygon_zoom.py -i /global/work/jsk/S800/norseas_800m_avg.nc_2006051212 -v h --xrange 1005:1262 --yrange 135:465 --var_min 217 --var_max 533 
```

the possible arguments corresponding to ranges of polygon area  are printed into terminal and can be copied and pasted:

```
the following arguments can be passed to the script for further zooming if needed:
--yrange  496:711  --xrange  1207:1330  --var_min  -1.81120717525  --var_max  -1.08693754673
```


![poly_zoom](poly_zoom0.png)

![polyzoom](poly_zoom1.png)

also it is possible to provide coordinate ranges in percents with ```--xzoom``` and ```--yzoom```:

```
python polygon_zoom.py -i /global/work/jsk/S800/norseas_800m_avg.nc_2006051212 -v h --xzoom 80:95 --yzoom 5:20 --var_min 217 --var_max 533 
```