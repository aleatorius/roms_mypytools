#!/usr/bin/python
import sys, re, glob
from os import system
mol = sys.argv[1]
file= 'qmudiamu'+mol+'.out'
string = "sed '/@ Quadratic/,/@omega B, omega C, QR value/p;d' "+file+" | sed '1~6 d' | sed '4~5 d' | sed 's/@.*[:|=]//' | sed 's/  [1|2] //'"+ "| sed \'N;N;N;s/\\n//g\'"


system(string)
