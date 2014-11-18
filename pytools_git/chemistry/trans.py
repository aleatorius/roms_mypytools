#!/usr/bin/python

import sys,os, re, glob
from numpy import array,vdot
from string import split

#mol = sys.argv[1]
xc = float(sys.argv[1])
yc = float(sys.argv[2])
zc = float(sys.argv[3])
shift = [xc,yc,zc]




#inp = open(mol+'.mol','r')
#out = open(mol+'_tr.mol', 'w')

for line in sys.stdin.readlines():
    spl = line.split()
    if len(spl)!=4: sys.stdout.write(line); continue
    try: vec = map(float,spl[1:])
    except: sys.stdout.write(line); continue
    vec = map(lambda (x,y): x-y, zip(vec,shift))
    print line[0], '%23.10f%23.10f%23.10f' % tuple(vec)
    
'''
atomtypes = os.popen("grep Atomtypes "+mol+'.mol').read()
atoms = (os.popen("grep Atoms "+mol+'.mol').read()).split()
print atoms
atypes = int(atomtypes.split('=')[1])
nlist = list()
print nlist
for i in range(1,atypes+1):
    print i
    nlist.append(int(atoms[2*i-1].split('=')[1]))
print nlist
vector = list()
hat = 6
for i in range(1,atypes+1):
    hat = hat + 1
    vector.extend(range(hat, hat + nlist[i-1]))
    hat = vector[-1]+1
print vector
    

count = 0
for line in inp.readlines():
    count = count + 1
    print count
    if count in vector:
        vec = map(float,line.split()[1:])
        print vec     
'''
