DRAFT

Files:
* [pyint_op.py](https://source.uit.no/mitya/pytools_git/blob/master/pyint_op.py)

 * to be replaced with totally numpified version: [pyint_array.py](https://source.uit.no/mitya/pytools_git/blob/master/pyint_array.py)

 * or with interactive version: [polygon_zoom_int.py](https://source.uit.no/mitya/pytools_git/blob/master/polygon_zoom_int.py)

* [biomass_q.sh](https://source.uit.no/mitya/pytools_git/blob/master/biomass_q.sh)

* [biomass_graph.py](https://source.uit.no/mitya/pytools_git/blob/master/biomass_graph.py)

Usage:

```
python pyint_op.py -i ocean_rst_2007_03_07.nc -v phytoplankton --graphics yes
```
it prints a mass value to "variable"_mass.txt by default. And it shows the plot.
```
qsub biomass_q.sh
```
it executes:
```
if foo="$(python pyint_op.py -v $bio --graphics no -i $file -o massq.txt)"; then
```
so it prints into "variable"_massq.txt. Plot is disabled by ```--graphics no```

To plot masses:
```
/global/work/mitya/run/Arctic-20km/archive_2005_rename
python biomass_graph.py -i _massq.txt
```

Sample outputs:


![meshplot](pyint_op.png)

![time_series](biomass_pzd.png)
