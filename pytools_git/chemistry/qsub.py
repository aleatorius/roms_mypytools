#!/usr/bin/python
import sys, re, glob
from string import split


for file in glob.glob('*.pbs_rep'):                 
    print '\n[%s]' % file
    
    from os import system
    system('qsub '+ file)
