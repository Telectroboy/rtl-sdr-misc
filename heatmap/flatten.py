#! /usr/bin/env python

"""#########################################################################################
### Programme pour comparaison de 2 fichiers avec entrée de la tolérance en variables    ###
###             Exemple python3 flatten.py riomoff.csv riomoff2.csv 10  				 ###
###           Pour comparer riomoff et riomoff2 avec une tolerance de 10%				 ###
###                 Faire acquisition avec rtl_power au préalable						 ###
### 	Exemple sudo rtl_power -f 0M:4M:1k -i 10s -c 0.25 -1 -g 50 "riomoff2.csv" -D2	 ###
############################################################################################			 
"""


import sys
import csv
import numpy as np			#numpy pour normaliser l'array
import os
from collections import defaultdict

# aide si nombre d'arguments incorrect 
def help():
    print("flatten.py 10")
    print("Execute une mesure sur RTLSDR et la compare avec les fichiers dans dataset + tolerance")
    sys.exit()

if len(sys.argv) < 1:
    help()

if len(sys.argv) > 2:
    help()

# argument apres commande flatten.py (nom du fichier .csv)
#path1 = sys.argv[1]  		#fichier1
#path2 = sys.argv[2]  		#fichier2
tolerance = sys.argv[1]

# definition des variables sums et counts
sums = defaultdict(float)
counts = defaultdict(int)
somme = 0
a = 0
row = []
row2 = []
compteur = 0

files = os.listdir('./dataset')  		#lecture des fichiers dans dataset
os.system('sudo rtl_power -f 0M:4M:1k -i 1s -c 0.25 -1 -g 50 "sample.csv" -D2')

def frange(start, stop, step):
    i = 0
    f = start
    while f <= stop:
        f = start + step*i
        yield f
        i += 1
		
### Lecture du Sample et stockage dans array rowrawsample_normed apres normalisation
for line in open('sample.csv'):
	line = line.strip().split(', ')     #separateur de ligne
	low = int(line[2])   				#low = frequence basse de la ligne lue colonne 2 (3 avec le 0)
	high = int(line[3])	 				#freq haute
	step = float(line[4])				#pas
	weight = int(line[5])				#poids?
	dbm = [float(d) for d in line[6:]]		# à déterminer
	for f,d in zip(frange(low, high, step), dbm):
		sums[f] += d*weight
		counts[f] += weight
        
ave = defaultdict(float)
for f in sums:
    ave[f] = sums[f] / counts[f]    

for f in sorted(ave):
	row.insert(a,float(ave[f]))
	a += 1

rowraw = np.array(row)
rowrawsample_normed= row / rowraw.min()


#### LECTURE DU PREMIER FICHIER stocké dans rowraw_normed
os.chdir('./dataset')
for file in files:
	print(file)
	for line in open(file):
		line = line.strip().split(', ')     #separateur de ligne
#		row = line
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

	# sortie dans la console uniquement de la valeur en dBm    
	for f in sorted(ave):
		row.insert(a,float(ave[f]))
		a += 1

	rowraw = np.array(row)
	rowraw_normed = row / rowraw.min()

##################################################### DETECTION DIFFERENCE ###############################################
	print("Comparaison au pas de", step, ("Hz"))
	while a > 0:
		a -= 1
		val = rowrawsample_normed[a]
		if val > (rowraw_normed[a] + (float(tolerance)/100)) or val < (rowraw_normed[a] - (float(tolerance)/100)) :
			#print(val)
			print ("raie trouvée à", a*step,"Hz", " différence =", (val-rowraw_normed[a])*100,"%")
			compteur += 1

	if compteur == 0:
		print ("Aucune différence détectée")
