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
    for f,d in zip(frange(low, high, step), dbm):    #Il "zip" les infos dans f et la valeur dans d
        sums[f] += d*weight
        counts[f] += weight

for line in open(path2):
    line = line.strip().split(', ')     #separateur de ligne
    low = int(line[2])   #low = frequence basse de la ligne lue colonne 2 (3 avec le 0)
    high = int(line[3])	 #freq haute
    step = float(line[4])	#pas
    weight = int(line[5])	#poids?
    dbm = [float(d) for d in line[6:]]		#comprends pas...
    for f,d in zip(frange(low, high, step), dbm):
        sums[f] += d*weight
        counts[f] += weight
        
ave = defaultdict(float)

for f in sums:
    ave[f] = sums[f] / counts[f]

# sortie dans la console uniquement de la valeur en dBm    
for f in sorted(ave):
    print(str(ave[f]))
    
# ecrit dans le fichier update.csv
    with open('update.csv', 'w') as outFile:
        outFile.write(str(ave[f]))
