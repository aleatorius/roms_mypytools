#!/usr/bin/python
import sys,os, glob
import numpy
from numpy import *
from os import system
mol = sys.argv[1]
basis = sys.argv[2]
file = 'data'

if mol == '4':
	alpha = 0.014671616126484271
elif mol == '1':
	alpha = 0.018331743961062276
elif mol == '3':
	        alpha = 0.029639878646195873
elif mol == '2':
	        alpha = 0.020050445731303185
else :
	print 'fuck yourslef';  sys.exit()

command = './cubic.py '+mol+ ' '+ basis+' > '+file
system(command)




inp_file = open(file, "r")
out_file = open(file+'_out', "w")
fstring = inp_file.read()
fstring = fstring.replace('ANGMOM', '').replace('DIPLEN','').replace('SECMOM','').replace('XX','0 0').replace('XY','0 1').replace('XZ','0 2').replace('YY','1 1').replace('YZ','1 2').replace('ZZ','2 2')
fstring = fstring.replace('X', '0').replace('Z', '2').replace('Y', '1')
out_file.write(fstring)
inp_file.close()
out_file.close()
inp_file = open(file+'_out', "r")
out_file = open(file+'_out1', "w")

a_dic = {}
g_dic = {}
for line in inp_file.readlines():
	st = line.split()
	if len(st) == 9:
		'print int(st[0]), int(st[2]), int(st[4]), int(st[6])'
		'G_para= -<<mu, m, m, mu>> = (DAAD)/4'
		g_dic[(int(st[0]), int(st[2]), int(st[4]), int(st[6]))]= float(st[8])/4.
		'print g_dic[(int(st[0]), int(st[2]), int(st[4]), int(st[6]))]'
	else:
		'print int(st[0]), int(st[2]), int(st[3]), int(st[5]), int(st[7])'
		'a = -i <<mu, q, m, mu>> = (DQAD)/2'
		a_dic[(int(st[0]), int(st[2]), int(st[3]), int(st[5]), int(st[7]))]= float(st[9])/2.
		a_dic[(int(st[0]), int(st[3]), int(st[2]), int(st[5]), int(st[7]))]=float( st[9])/2.
		'print a_dic[(int(st[0]), int(st[2]), int(st[3]), int(st[5]), int(st[7]))]'
inp_file.close()
out_file.close()



'define eps'
eps = {(0,1,2): 1, (0,2,1): -1, (1,0,2): -1, (1,2,0): 1,  (2,0,1): 1, (2,1,0): -1}
sum = 0
for i in range(0,3):
	for j in range(0,3):
		for k in range(0,3):
			
			sum = sum + eps.get((i,j,k),0)*eps.get((i,j,k),0)

alf_p = 0
for i in range(0,3):
	for j in range(0,3):
		for k in range(0,3):
			for l in range(0,3):
				alf_p = alf_p + eps.get((i,j,k),0)*(a_dic.get((i,j,l,l,k),0)+a_dic.get((i,j,l,k,l),0))
'print alf_p'

file = 'data2'
command = './qmudiamu.py '+mol+' '+basis+' > '+file
system(command)
inp_file = open(file, "r")
out_file = open(file+'_out', "w")
fstring = inp_file.read()
fstring = fstring.replace('DIPLEN','').replace('SUSCGO','').replace('XX','0 0').replace('XY','0 1').replace('XZ','0 2').replace('YY','1 1').replace('YZ','1 2').replace('ZZ','2 2')
fstring = fstring.replace('X', '0').replace('Z', '2').replace('Y', '1')
out_file.write(fstring)
inp_file.close()
out_file.close()

inp_file = open(file+'_out', "r")
out_file = open(file+'_out1', "w")

dia_dic = {}
for line in inp_file.readlines():
	st = line.split()
	'G_dia = <<mu,xi,mu>> = -(DSD)'
	dia_dic[(int(st[0]), int(st[2]), int(st[3]), int(st[5]))]= -float(st[9])
	dia_dic[(int(st[0]), int(st[3]), int(st[2]), int(st[5]))]= -float(st[9])
	'print int(st[0]), int(st[2]), int(st[3]), int(st[5])'
	'print dia_dic[(int(st[0]), int(st[2]), int(st[3]), int(st[5]))]'
		
inp_file.close()
out_file.close()

G_dic = {}
'G = G_para+ G_dia'
for i in range(0,3):
	for j in range(0,3):
		for k in range(0,3):
			for l in range(0,3):
				G_dic[(i,j,k,l)] = dia_dic.get((i,j,k,l),0) + g_dic.get((i,j,k,l),0)


g_p = 0
for i in range(0,3):
	for j in range(0,3):
		g_p = g_p + 3.*G_dic[(i,j,i,j)]+3.*G_dic[(i,j,j,i)]-2.*G_dic[(i,i,j,j)]
ralf_p =  alf_p*0.072/2.
print 'g part = 3G+3G-2G:      ', g_p, '\na part = (omega/2)*eps.(a+a):     ', ralf_p, '\nresult = (g_part - a_part):   ', (g_p-ralf_p)

out_fin = open('table.ptex'+mol, "a")
string =  basis +  ' & '+ str(g_p) +  ' & ' + str(ralf_p)+ ' & ' + str((g_p-ralf_p)/1000.) +' & ' + str((g_p-ralf_p)*alpha/10.)+ '\\'+'\\'+'\n'
print string
out_fin.write(string)
out_fin.close()
