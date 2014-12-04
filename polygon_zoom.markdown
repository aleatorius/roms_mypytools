DRAFT

#### Files:

* [polygon_zoom.py](https://source.uit.no/mitya/pytools_git/blob/master/polygon_zoom.py) 

#### Description:

The polygon area can be picked. The rectangular mesh grid containing the polygon area is created. The range of a colobar is defined by the interior points of this polygon area - thus this tool can be used just for purpose of finding out of ranges within area of interest.


#### Usage:
 
```
python polygon_zoom.py -i /global/work/jsk/S800/norseas_800m_avg.nc_2006123012 -v temp
```
Left-clicks add vertices to the line - it results to a segmented line. Line can pass through masked area.

A right-click puts this process to the end and fires a window with two plots.

The colorbar range is defined by interior points of the polygon area.

### Sample outputs:

![poly_zoom](poly0.png)

NB: the date can be corrected by making changes in this line: ```ref = date(1970,01,01)```

![polyzoom](poly1.png)

Bathymetry zoom (impose masking?):

![poly_zoom](poly2.png)

![polyzoom](poly3.png)

It is possible to zoom further on, in the following way:

```
python polygon_zoom.py -i /global/work/jsk/S800/norseas_800m_avg.nc_2006051212 -v h --xrange 1005:1262 --yrange 135:465 --var_min 217 --var_max 533 
```

![poly_zoom](poly_zoom0.png)

![polyzoom](poly_zoom1.png)

also it is possible to provide coordinate ranges in percents with ```--xzoom``` and ```--yzoom```:

```
python polygon_zoom.py -i /global/work/jsk/S800/norseas_800m_avg.nc_2006051212 -v h --xzoom 80:95 --yzoom 5:20 --var_min 217 --var_max 533 
```