DRAFT

Files:

* [line_zoom.py](https://github.com/aleatorius/roms_mypytools/blob/master/pytools_git/line_zoom.py) 


Usage:
 
```
python line_zoom.py -i /global/work/jsk/S800/norseas_800m_avg.nc_2006123012 -v temp
```
Left-clicks add vertices to the line - it results to a segmented line. Line can pass through masked area.

A right-click puts this process to the end and fires a window with two plots.

There are some other options available:
```
python line_zoom.py -i /global/work/jsk/S800/norseas_800m_avg.nc_2006123012 -v temp --contourf yes
```


### Sample outputs:

![line_zoom](line_zoom_0.png)

NB: the date can be corrected by making changes in this line: ```ref = date(1970,01,01)```

![line_zoom](line_zoom.png)


`--contourf yes`
![line_zoom](line_zoom_cf.png)
