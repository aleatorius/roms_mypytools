#### 2d mesh plot along specified s-coordinate (--vert)

NB: if you need to zoom - use this one instead:

https://source.uit.no/mitya/pytools_git/wikis/polygon_zoom

Files:
* [pyview](https://source.uit.no/mitya/pytools_git/blob/master/pyview)
** command line interactivity - suitable for scripts and printing
* [pyview_nb](https://source.uit.no/mitya/pytools_git/blob/master/pyview_nb)
** command line and GUI interactivity - can navigate vertical layers and time records (4d variables and 3d variables). 

Usage:
```
               [mitya@stallo-1 1993_2010_jens]$ pyview -h
pyview [-h] [-i INF] [-v VARIABLE] [-f TIME_F] [--time_rec TIME_REC]
              [--time TIME] [--vert VERT] [--xzoom XZOOM] [--yzoom YZOOM]
              [--var_min VAR_MIN] [--var_max VAR_MAX]
 
pyview 0.1
 
optional arguments:
  -h, --help           show this help message and exit
  -i INF               input file
  -v VARIABLE          variable
  -f TIME_F            time format
  --time_rec TIME_REC  time rec
  --time TIME          time counter
  --vert VERT          vertical coordinate number
  --xzoom XZOOM        zoom along x(?) direction, range is defined in percents
  --yzoom YZOOM        zoom along y(?) direction, range is defined in percents
  --var_min VAR_MIN    minimum value of variable
  --var_max VAR_MAX    minimum value of variable
```

```--vert 0``` gives a bottom sigma layer (rho-points), ```--vert 34``` gives surface layer (in our ROMS appas, where there is 35 vertical layers). The latest case is the default one.

Example:
```
python ~/pytools_git/pyview -i archive_2005_rename/ocean_avg_0013_2005_05_26.nc -v NO3 --vert 0
python ~/pytools_git/pyview -i archive_2005_rename/ocean_avg_0013_2005_05_26.nc -v NO3 --vert 30
```

### Sample outputs:

`--vert 0`
![pyview](pyview1.png)

`--vert 30`
![pyview](pyview2.png)

A mouse-click gives the value of a variable:

![pyview](click.png)

Graphically interactive (buttons):

* left-right arrows for time records (mostly)
* up-down arrows for vertical leayers

4d variable:

```
python pyview_nb -i /global/work/apn/S800_short/norseas_800m_avg_2058.nc -v temp --ref_datetime 1948-01-01 00:00:00
```

![pyview](4d_1.png)

![pyview](4d_2.png)

3d variable:

```
python pyview_nb -i /global/work/apn/S800_short/norseas_800m_avg_2058.nc -v hice --ref_datetime 1948-01-01 00:00:00
```

![pyview](3d.png)

