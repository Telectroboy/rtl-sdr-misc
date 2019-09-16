#! /usr/bin/env python

import sys
import csv
import numpy as np			#numpy pour normaliser l'array
from collections import defaultdict

# aide si nombre d'arguments incorrect 
def help():
    print("flatten.py input.csv")
    print("turns any rtl_power csv into a more compact summary")
    sys.exit()

if len(sys.argv) <= 2:
    help()

if len(sys.argv) > 3:
    help()

# argument apres commande flatten.py (nom du fichier .csv)
path1 = sys.argv[1]  #fichier1
path2 = sys.argv[2]  #fichier2

# definition des variables sums et counts
sums = defaultdict(float)
counts = defaultdict(int)
somme = 0
a = 0
row = []
row2 = []

def frange(start, stop, step):
    i = 0
    f = start
    while f <= stop:
        f = start + step*i
        yield f
        i += 1

for line in open(path1):
	line = line.strip().split(', ')     #separateur de ligne
#	row = line
	low = int(line[2])   #low = frequence basse de la ligne lue colonne 2 (3 avec le 0)
	high = int(line[3])	 #freq haute
	step = float(line[4])	#pas
	weight = int(line[5])	#poids?
	dbm = [float(d) for d in line[6:]]		#
	for f,d in zip(frange(low, high, step), dbm):
		sums[f] += d*weight
		counts[f] += weight

        
ave = defaultdict(float)
for f in sums:
    ave[f] = sums[f] / counts[f]
    
c=0
# sortie dans la console uniquement de la valeur en dBm    
for f in sorted(ave):
# 	somme = somme + float(ave[f])   #plus utilise
#	print(float(ave[f]))
#	print(float(somme))
#	c += 1				#compteur du nombre de pour faire la moyenne Plus utilise
	row.insert(a,float(ave[f]))
	a += 1
	
# ecrit dans le fichier update.csv
with open('update.csv', 'w', ) as outFile:
	write = csv.writer(outFile, delimiter=',')
	outFile.write(str(row))
	print(row)	

"""			PLUS UTILISE!
moyenne = somme / c
print(float(moyenne))			#affichage de la valeur moyenne
"""


rowraw = np.array(row)
rowraw_normed= row / rowraw.min()
# print rowraw.min() affichage de la valeur max (tout est negatif donc le max est un min)
print(rowraw_normed)  #affichage des valeurs normalisees de 0 a 1

################################################## SECOND FICHIER ######################################################
for line in open(path2):
	line = line.strip().split(', ')     #separateur de ligne
#	row = line
	low = int(line[2])   #low = frequence basse de la ligne lue colonne 2 (3 avec le 0)
	high = int(line[3])	 #freq haute
	step = float(line[4])	#pas
	weight = int(line[5])	#poids?
	dbm = [float(d) for d in line[6:]]		#
	for f,d in zip(frange(low, high, step), dbm):
		sums[f] += d*weight
		counts[f] += weight

ave = defaultdict(float)
for f in sums:
    ave[f] = sums[f] / counts[f]
	
for f in sorted(ave):
	row2.insert(a,float(ave[f]))
	a += 1
	
row2raw = np.array(row2)
row2raw_normed = row2 / row2raw.min()
print(row2raw_normed)  #affichage des valeurs normalisees de 0 a 1

##################################################### DETECTION DIFFERENCE ###############################################

	
