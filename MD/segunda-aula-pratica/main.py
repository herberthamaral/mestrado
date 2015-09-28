# encoding: utf-8
import math
from itertools import cycle
from queue import PriorityQueue
from dataset import load_dataset
import matplotlib.pyplot as plt

media = lambda x: sum(x)/float(len(x))

# euclidean distance
ed = lambda p1,p2: math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

#absolute standard deviation
asd = lambda x: sum([abs(xi - media(x)) for xi in x])/float(len(x))

#modified standard score (para normalização)
def msd(x):
    _asd = asd(x)
    mu = media(x)
    return [(xi - mu)/_asd for xi in x]

dset = load_dataset('iris.data')
x = msd(dset.T[0].astype(float))
y = msd(dset.T[1].astype(float))

pontos = [(x[i], y[i]) for i in range(len(x))]

clusters = PriorityQueue()
for i, p1 in enumerate(pontos):
    distancias = []
    for j,p2 in enumerate(pontos):
        distancia = (ed(p1,p2), p1, p2)
        if i != j and distancia not in distancias:
            distancias.append(distancia)

distancias.sort()
ciclo_cores = cycle(['r', 'g', 'b', 'y',])
ciclo_formas = cycle(['o', 'd', '*', '8', 's'])

[plt.plot([d[1][0], d[1][1]], [d[2][0], d[2][1]], ciclo_cores.next()) for d in distancias]
plt.show()
