#!/usr/bin/env python 
# -*- coding: utf-8 -*-
##!/home/ntnu/mitya/virt_env/virt1/bin/python -B
## Dmitry Shcherbin, 2014.07.01
##with navigation buttons, 2015.01.05
import numpy as np
from numpy import *
import sys, re, glob, os
import numpy.ma as ma
import argparse
import os.path


file_list1 = sorted(glob.glob("salt_a20/*"))
file_list2 = sorted(glob.glob("salt_a4/*"))

if len(file_list1)==0:
    print "list is empty"
    exit()
else:
    pass

start1= file_list1.index("salt_a20/hice_ocean_avg_0238_02.png")
start2 = file_list2.index("salt_a4/hice_ocean_avg_0219_1999_07_15_00.png")

len_of_list1 = len(file_list1)-start1
len_of_list2 = len(file_list2)-start2


for i in range(0, min(len_of_list1,len_of_list2)):

    
    print file_list1[i+start1], file_list2[i+start2]
    if i in range(0,10):
        counter="000"+str(i)
    elif i in range(10,100):
        counter="00"+str(i)
    elif i in range(100,1000):
        counter="0"+str(i)
    else:
        counter=str(i)
    os.system("convert "+file_list1[i+start1]+" "+file_list2[i+start2]+" +append "+ "a4_a20/salt_a4_a20_"+counter+".jpg" )



