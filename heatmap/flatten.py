#! /usr/bin/env python

"""#########################################################################################
### Programme pour comparaison de 2 fichiers avec entree de la tolerance en variables    ###
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
    print("flatten.py input.csv")
    print("turns any rtl_power csv into a more compact summary")
    sys.exit()

if len(sys.argv) <= 3:
    help()

if len(sys.argv) > 4:
    help()

# argument apres commande flatten.py (nom du fichier .csv)
path1 = sys.argv[1]  #fichier1
path2 = sys.argv[2]  #fichier2
tolerance = sys.argv[3]

# definition des variables sums et counts
sums = defaultdict(float)
counts = defaultdict(int)
somme = 0
a = 0
row = []
row2 = []
compteur = 0

os.system('sudo rtl_power -f 0M:4M:1k -i 1s -c 0.25 -1 -g 50 "sample.csv" -D2')

def frange(start, stop, step):
    i = 0
    f = start
    while f <= stop:
        f = start + step*i
        yield f
        i += 1

### Lecture du Sample et stockage dans array rowrawsample_normed apres normalisation
for line in open(sample.csv):
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


#### LECTURE DU PREMIER FICHIER  stocké dans 
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

# sortie dans la console uniquement de la valeur en dBm    
for f in sorted(ave):
	row.insert(a,float(ave[f]))
	a += 1

"""	  PLUS UTILISE
# ecrit dans le fichier update.csv
with open('update.csv', 'w', ) as outFile:
	write = csv.writer(outFile, delimiter=',')
	outFile.write(str(row))
#	print(row)	#utilise pour debug


			PLUS UTILISE!
moyenne = somme / c
print(float(moyenne))			#affichage de la valeur moyenne
"""


rowraw = np.array(row)
rowraw_normed= row / rowraw.min()
#print rowraw.min()  		#affichage de la valeur max (tout est negatif donc le max est un min)
#print(rowraw_normed)  		#affichage des valeurs normalisees de 0 a 1

################################################## SECOND FICHIER ######################################################
a = 0
for line in open(path2):
	line = line.strip().split(', ')     #separateur de ligne
	low = int(line[2])   #low = frequence basse de la ligne lue colonne 2 (3 avec le 0)
	high = int(line[3])	 #freq haute
	step = float(line[4])	#pas
	weight = int(line[5])	#poids
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
#print(row2raw_normed)  			#affichage des valeurs normalisees de 0 a 1

##################################################### DETECTION DIFFERENCE ###############################################
print("Comparaison au pas de", step, ("Hz"))
#print(step,"Hz") #affiche les pas pour Debug
#print(a,"nombre de points")
while a > 0:
	a -= 1
	val = row2raw_normed[a]
	if val > (rowraw_normed[a] + (float(tolerance)/100)) or val < (rowraw_normed[a] - (float(tolerance)/100)) :
		#print(val)
		print ("raie trouvée à", a*step,"Hz", " différence =", (val-rowraw_normed[a])*100,"%")
		compteur += 1
if compteur == 0:
	print ("Aucune différence détectée")
		
"""	 if val < (rowraw_normed[a] - (float(tolerance)/100)):
		#print(val)
		print ("raie trouvée à", a*step,"kHz"," différence =", (val-rowraw_normed[a])*100,"%")
"""
