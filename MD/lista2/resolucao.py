# encoding: utf-8
import numpy as np
import matplotlib.pyplot as plt
from dataset import load_dataset
from kmeans import kmeans

def minmax(x, xi):
    return (float(xi) - min(x))/(float(max(x))-min(x))

def z_score(x, xi):
    xbarra = np.median(x)
    numerador = xi-xbarra
    return numerador/np.std(x)

def questao21():
    dset = load_dataset('dataset1.csv')
    xo = dset.T[1].astype(float) # segunda coluna
    x = dset.T[1].astype(float) # segunda coluna
    yo = dset.T[2].astype(float) # terceira coluna
    y = dset.T[2].astype(float) # terceira coluna

    # a normalização com z-score ajudou na visualização e é necessária para agrupamento
    #x = [z_score(x, xi) for xi in x]
    #y = [z_score(y, yi) for yi in y]
    #centros_iniciais = [(z_score(xo, 1), z_score(yo, 2)), (z_score(xo, 4), z_score(yo, 2))]

    centros_iniciais = [(1,2), (4,2)]
    pontos = zip(x, y)

    clusters, iteracoes = kmeans(pontos, 2, centros_iniciais=centros_iniciais)

    cluster1 = clusters[0].pontos
    cluster2 = clusters[1].pontos
    plt.plot([xi[0] for xi in cluster1], [yi[1] for yi in cluster1], 'ro')
    plt.plot([clusters[0].centroide[0]], [clusters[0].centroide[1]], 'r*')
    plt.plot([xi[0] for xi in cluster2], [yi[1] for yi in cluster2], 'go')
    plt.plot([clusters[1].centroide[0]], [clusters[1].centroide[1]], 'g*')
    plt.savefig('grupo1.png')
    print "Novos centróides:", clusters[0].centroide, " e ", clusters[1].centroide

def flatten(vetor):
    flat = []
    for v in vetor:
        if type(v) not in (tuple, list):
            flat.append(v)
        else:
            flat.extend(flatten(v))
    return flat

print questao22()
