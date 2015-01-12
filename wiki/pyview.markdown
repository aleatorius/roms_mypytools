#### 2d mesh plot along specified s-coordinate (--vert)

Files:
* [pyview](https://github.com/aleatorius/roms_mypytools/blob/master/pytools_git/pyview)
  *  it has a command line interactivity - suitable for scripts and printing
* [pyview_nb](https://github.com/aleatorius/roms_mypytools/blob/master/pytools_git/pyview_nb)
  * it has a command line and GUI interactivity - a user can navigate vertical layers and time records (4d variables and 3d variables). 

* [pyview_list](https://github.com/aleatorius/roms_mypytools/blob/master/pytools_git/pyview_line)
  * A modified version of [pyview_nb](https://source.uit.no/mitya/pytools_git/blob/master/pyview_nb) - user can navigate along time records through the list of files.


### Graphically interactive script [pyview_nb](https://github.com/aleatorius/roms_mypytools/blob/master/pytools_git/pyview_nb) 

( with navigation buttons):


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


* left-right arrows for time records (mostly)
* up-down arrows for vertical layers
* note: the action of arrows is cyclic - if you reach the final (the first) time record or final (the first) vertical layer the next click in the same button will bring you back to the beginning (the end).

#### The case of a 4d variable:

```
python pyview_nb -i /global/work/apn/S800_short/norseas_800m_avg_2058.nc -v temp --ref_datetime 1948-01-01 00:00:00
```

![pyview](4d_1.png)

![pyview](4d_2.png)

#### The case of a 3d variable:

```
python pyview_nb -i /global/work/apn/S800_short/norseas_800m_avg_2058.nc -v hice --ref_datetime 1948-01-01 00:00:00
```

![pyview](3d.png)

### Graphically interactive script on the list of files [pyview_list](https://github.com/aleatorius/roms_mypytools/blob/master/pytools_git/pyview_line) 


```
python pyview_list -list /global/work/mitya/run/Arctic-20km/archive_2005_cortemp/ocean_avg_*2005 -start /global/work/mitya/run/Arctic-20km/archive_2005_cortemp/ocean_avg_*2005*0034 -v hice
```

* a list is specified by the prefix ```-list```:

```
-list /global/work/mitya/run/Arctic-20km/archive_2005_cortemp/ocean_avg_*2005
```

The script creates and prints the following sorted list:

```
0 /global/work/mitya/run/Arctic-20km/archive_2005_cortemp/ocean_avg_0001_2005_01_26.nc
1 /global/work/mitya/run/Arctic-20km/archive_2005_cortemp/ocean_avg_0002_2005_02_05.nc
2 /global/work/mitya/run/Arctic-20km/archive_2005_cortemp/ocean_avg_0003_2005_02_15.nc
3 /global/work/mitya/run/Arctic-20km/archive_2005_cortemp/ocean_avg_0004_2005_02_25.nc
4 /global/work/mitya/run/Arctic-20km/archive_2005_cortemp/ocean_avg_0005_2005_03_07.nc
5 /global/work/mitya/run/Arctic-20km/archive_2005_cortemp/ocean_avg_0006_2005_03_17.nc
...
31 /global/work/mitya/run/Arctic-20km/archive_2005_cortemp/ocean_avg_0032_2005_12_02.nc
32 /global/work/mitya/run/Arctic-20km/archive_2005_cortemp/ocean_avg_0033_2005_12_12.nc
33 /global/work/mitya/run/Arctic-20km/archive_2005_cortemp/ocean_avg_0034_2005_12_22.nc
34 /global/work/mitya/run/Arctic-20km/archive_2005_cortemp/ocean_avg_2005_12_22_0034.nc
```
A starting file is specified with the prefix ```-start```:

```
-start /global/work/mitya/run/Arctic-20km/archive_2005_cortemp/ocean_avg_*2005*0034
```

To navigate along time record user should click left and right arrows, if the last or first record of the current file is reached scripts jumps to the next or previous file. If this the last or first file in the list - it jumps to the first or last file of the list (cyclic). Scripts doesn't store all the data - it iterates through the files.

To navigate along vertical layers user should click up and down arrows. 



### The command line interactive script [pyview](https://github.com/aleatorius/roms_mypytools/blob/master/pytools_git/pyview):

Example:
```
python ~/pytools_git/pyview -i archive_2005_rename/ocean_avg_0013_2005_05_26.nc -v NO3 --vert 0 --time 3
python ~/pytools_git/pyview -i archive_2005_rename/ocean_avg_0013_2005_05_26.nc -v NO3 --vert 30
```

#### Sample outputs:

`--vert 0`
![pyview](pyview1.png)

`--vert 30`
![pyview](pyview2.png)

A mouse-click gives the value of a variable:

![pyview](click.png)
