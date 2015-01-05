#### 2d mesh plot along specified s-coordinate (--vert)

NB: if you need to zoom to a curved area - use this script instead:
  * https://source.uit.no/mitya/pytools_git/wikis/polygon_zoom

Files:
* [pyview](https://source.uit.no/mitya/pytools_git/blob/master/pyview)
  *  it has a command line interactivity - suitable for scripts and printing
* [pyview_nb](https://source.uit.no/mitya/pytools_git/blob/master/pyview_nb)
  * it has a command line and GUI interactivity - a user can navigate vertical layers and time records (4d variables and 3d variables). 

Usage:
```
[mitya@stallo-2 pytools_git]$ python pyview_nb -h
usage: python pyview_nb -i /global/work/apn/S800_short/norseas_800m_avg_2058.nc -v hice --xzoom 50:100 --yzoom 50:100  --ref_datetime 1948-01-01 00:00:00

pyview_nb

optional arguments:
  -h, --help            show this help message and exit
  -i INF                input file
  -v VARIABLE           variable
  --ref_datetime REF_DATETIME REF_DATETIME
                        reference date time: 1970-01-01 00:00:00
  -f TIME_F             time format
  --time_rec TIME_REC   time rec
  --time TIME           time counter
  --vert VERT           vertical coordinate number
  --xzoom XZOOM         zoom along x direction, range is defined in percents
  --yzoom YZOOM         zoom along y direction, range is defined in percents
  --var_min VAR_MIN     minimum value of variable
  --var_max VAR_MAX     minimum value of variable
```

```--vert 0``` gives a bottom sigma layer (rho-points), ```--vert 34``` gives surface layer (in our ROMS appas, where there is 35 vertical layers). The latest case is the default one.


Graphically interactive script [pyview_nb](https://source.uit.no/mitya/pytools_git/blob/master/pyview_nb) 

( with navigation buttons):

* left-right arrows for time records (mostly)
* up-down arrows for vertical layers
* note: the action of arrows is cyclic - if you reach the final (the first) time record or final (the first) vertical layer the next click in the same button will bring you back to the beginning (the end).

The case of a 4d variable:

```
python pyview_nb -i /global/work/apn/S800_short/norseas_800m_avg_2058.nc -v temp --ref_datetime 1948-01-01 00:00:00
```

![pyview](4d_1.png)

![pyview](4d_2.png)

The case of a 3d variable:

```
python pyview_nb -i /global/work/apn/S800_short/norseas_800m_avg_2058.nc -v hice --ref_datetime 1948-01-01 00:00:00
```

![pyview](3d.png)

The command line interactive script [pyview](https://source.uit.no/mitya/pytools_git/blob/master/pyview):

Example:
```
python ~/pytools_git/pyview -i archive_2005_rename/ocean_avg_0013_2005_05_26.nc -v NO3 --vert 0 --time 3
python ~/pytools_git/pyview -i archive_2005_rename/ocean_avg_0013_2005_05_26.nc -v NO3 --vert 30
```

### Sample outputs:

`--vert 0`
![pyview](pyview1.png)

`--vert 30`
![pyview](pyview2.png)

A mouse-click gives the value of a variable:

![pyview](click.png)