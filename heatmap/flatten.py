#! /usr/bin/env python

import sys
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
def frange(start, stop, step):
    i = 0
    f = start
    while f <= stop:
        f = start + step*i
        yield f
        i += 1

for line in open(path1):
    line = line.strip().split(', ')     #separateur de ligne
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
   	somme = somme + float(ave[f])
	print(float(ave[f]))
	print(float(somme))
	c += 1				#compteur du nombre de pour faire la moyenne
    
# ecrit dans le fichier update.csv
    	with open('update.csv', 'w') as outFile:
    		outFile.write(str(ave[f]))

moyenne = somme / c
print(float(moyenne))
