#!/usr/bin/python
import sys, re, glob
from os import system
mol = sys.argv[1]
file = 'c'+mol+'.out'
string = "sed '/@ Cubic/,/@ << A/p;d'"+" "+file+"     | sed '1~7 d' | sed '5~6 d' | sed 's/@.*[:|=]//' | sed 's/  [1|2] //' | sed 'N;N;N;N;s/\\n//g'"

system(string)
