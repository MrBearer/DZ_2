"""
Scheme Checking
"""

from xml.dom.minidom import parse
import csv
import sys
from fast_graph import fast_fl

XML_FILE = parse(sys.argv[1])
ELEMENT_REF = XML_FILE.getElementsByTagName('resistor')
G = []
i = 0
for resistor in ELEMENT_REF:
    G.append([0]*4)
    G[i][0] = 'r'
    G[i][1] = int(resistor.attributes["net_from"].value)-1
    G[i][2] = int(resistor.attributes["net_to"].value)-1
    G[i][3] = float(resistor.attributes["resistance"].value)
    i = i+1
ELEMENT_REF = XML_FILE.getElementsByTagName('capactor')
for capactor in ELEMENT_REF:
    G.append([0]*4)
    G[i][0] = 'c'
    G[i][1] = int(capactor.attributes["net_from"].value)-1
    G[i][2] = int(capactor.attributes["net_to"].value)-1
    G[i][3] = float(capactor.attributes["resistance"].value)
    i = i+1
ELEMENT_REF = XML_FILE.getElementsByTagName('diode')
for resistor in ELEMENT_REF:
    G.append([0]*5)
    G[i][0] = 'd'
    G[i][1] = int(resistor.attributes["net_from"].value)-1
    G[i][2] = int(resistor.attributes["net_to"].value)-1
    G[i][3] = float(resistor.attributes["resistance"].value)
    G[i][4] = float(resistor.attributes["reverse_resistance"].value)
    i = i+1
D = []
ELEMENT_REF = XML_FILE.getElementsByTagName('net')
N = len(ELEMENT_REF)
for j in range(N):
    D.append([float('Inf')] * N)
for j in range(N):
    D[j][j] = 0
for j in range(i-1):
    if G[j][0] != 'd':
        D[G[j][1]][G[j][2]] = 1 / (1 / D[G[j][1]][G[j][2]] + 1 / G[j][3])
        D[G[j][2]][G[j][1]] = D[G[j][1]][G[j][2]]
    else:
        D[G[j][1]][G[j][2]] = 1 / (1 / D[G[j][1]][G[j][2]] + 1 / G[j][3])
        D[G[j][2]][G[j][1]] = 1 / (1 / D[G[j][2]][G[j][1]] + 1 / G[j][4])

D = fast_fl(D)

with open(sys.argv[2], 'w', newline='') as csvfile:
    CSV_WRITER = csv.writer(csvfile, delimiter=',')
    for l in D:
        CSV_WRITER.writerow(["%.6f" % item for item in l])
