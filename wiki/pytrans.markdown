## Transections 

Files:

* [pytrans_write.py](https://source.uit.no/mitya/pytools_git/blob/master/pytrans_write.py) 
* [pytrans.py](https://source.uit.no/mitya/pytools_git/blob/master/pytrans.py)
  * a modified version of [pytrans_write.py](https://source.uit.no/mitya/pytools_git/blob/master/pytrans_write.py): everything is in one widnow, no pop-ups. 
* [pytrans_read.py](https://source.uit.no/mitya/pytools_git/blob/master/pytrans_read.py)

Copy files [pytrans_write.py](https://source.uit.no/mitya/pytools_git/blob/master/pytrans_write.py) and [pytrans_read.py](https://source.uit.no/mitya/pytools_git/blob/master/pytrans_read.py) to your directory.

Usage:
 
```
python pytrans_write.py -i ocean_avg_0013.nc -v salt &
```
Left-clicks add vertices to the line - it results to a segmented line. Line can pass through masked area.

A right-click puts this process to the end - it results to a transectional vertical plot plus to s-layers plot and txt file `segments`. 
A double click kills all graphics windows.

Mesh data are linearly interpolated vertically.

NB: If one starts a new line - old txt file will be rewritten.

Segments can be read by (txt file `segments` is read by default)
```
python pytrans_read.py -i ocean_avg_0013.nc -v temp &
```
The txt-file `segments` should be renamed if the specific path is required for further usage (to plot other variables or for another date).

This renamed txt file, e.g. `segments_fram`, can be passed to pytrans_read.py as an argument with `-is` prefix:
```
 python pytrans_read.py -i ocean_avg_0013.nc -v salt -is segments_fram &
```
File `segments` can be modified manually, pay attention that lat lon written by `pytrans_write.py`are optional - they are just for reference - they are not read. So the content of this file should look like:
```
(100,10)
(300,240)
(67,123)
```


There are some other options available:
```
python pytrans_read.py -i ocean_avg_0013.nc -v salt --extras yes --contourf yes & 

python pytrans_read.py -i ocean_avg_2006_05_21_0049.nc -v phytoplankton --depth_max 200 --depth_min 10 --contourf yes
```


### Sample outputs:

![pytrans](pytrans1.png)

![pytrans](pytrans3.png)

`--extras yes`
![pytrans](pytrans2.png)


`--contourf yes`
![pytrans](pytrans4.png)

`--depth_max 200 --depth_min 10`
![pytrans](phyto_depth.png)

```
python pytrans.py -i /global/work/mitya/run/Arctic-20km/archive_2005_cortemp/ocean_avg_2005_12_22_0034.nc -v temp  &
```

![pytrans](pytrans_nopop.png)

