# encoding: utf-8
from itertools import cycle
import sys, math, random
import matplotlib.pyplot as plt
import numpy as np
from dataset import load_dataset

# euclidean distance
ed = lambda p1,p2: math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

class Cluster(object):
    def __init__(self, pontos):
        self.pontos =  pontos
        self.centroide = self.calcula_centroide()

    def __repr__(self):
        return "<Cluster "+str(self.pontos)+">"

    def update(self, pontos):
        centroide_anterior = self.centroide
        self.pontos = pontos 
        self.centroide = self.calcula_centroide()
        return ed(centroide_anterior, self.centroide)

    def calcula_centroide(self):
        obtem_somatorio_coluna = lambda i: sum(p[i] for p in self.pontos)
        coordenadas_centroide= [obtem_somatorio_coluna(i)/len(self.pontos) for i in range(len(self.pontos[0]))] 
        return coordenadas_centroide

def kmeans(pontos, num_classes, criterio_parada=0.5):
    centroides_iniciais = random.sample(pontos, num_classes)
    # cria os clusters com apenas um ponto aleatório para depois ajusta-lo
    clusters = [Cluster([p]) for p in centroides_iniciais]
    iteracoes = 0
    while True:
        iteracoes += 1
        lists = [ [] for c in clusters]
        for p in pontos:
            menor_distancia = ed(p, clusters[0].centroide)
            index = 0
            for i in range(len(clusters[1:])):
                distancia = ed(p, clusters[i+1].centroide)
                if distancia < menor_distancia:
                    menor_distancia = distancia 
                    index = i+1
            lists[index].append(p)
        maior_mudanca = 0.0
        for i in range(len(clusters)):
            mudanca = clusters[i].update(lists[i])
            maior_mudanca = max(maior_mudanca, mudanca)
        if maior_mudanca < criterio_parada: 
            print "parando depois de ", iteracoes, " iterações"
            break
    return clusters

def cria_ponto_aleatorio(n, lower, upper):
    return [random.uniform(lower, upper) for i in range(n)]

def main():
    dataset = load_dataset('iris.data')
    pontos = [[float(linha[0]), float(linha[1])] for linha in dataset]
    num_classes, criterio_parada = 8, 0.01
    clusters = kmeans(pontos, num_classes, criterio_parada)
    
    cores = ['r', 'g', 'b', 'y']
    formas = ['o', '*', '^']
    coresxformas = [c+f for f in formas for c in cores]

    for i,c in enumerate(clusters): 
        for p in c.pontos:
            print "Cluster ",i, "Ponto ", p, " forma ", coresxformas[i]
            plt.plot([p[0]], [p[1]], coresxformas[i])
    plt.show()

if __name__ == "__main__": 
    main()
