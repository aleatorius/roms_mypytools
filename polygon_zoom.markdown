DRAFT

Files:

* [polygon_zoom.py](https://source.uit.no/mitya/pytools_git/blob/master/polygon_zoom.py) 

Usage:
 
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