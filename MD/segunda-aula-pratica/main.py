# encoding: utf-8
from itertools import cycle
import sys, math, random
import matplotlib.pyplot as plt
import numpy as np
from dataset import load_dataset

# euclidean distance
ed = lambda p1,p2: math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

class Cluster(object):
    ficou_sem_ponto = False
    def __init__(self, pontos):
        self.pontos =  pontos
        self.centroide = self.calcula_centroide()

    def __repr__(self):
        return "<Cluster "+str(self.pontos)+">"

    def update(self, pontos):
        self.centroide_anterior = self.centroide
        self.pontos = pontos 
        if len(pontos) > 0:
            self.centroide = self.calcula_centroide()
            return ed(self.centroide_anterior, self.centroide)
        else: #caso o centróide não tenha nenhum ponto próximo...
            self.ficou_sem_ponto = True
            return 1 #... faz com que ele seja movido através de uma pertubação

    def calcula_centroide(self):
        obtem_somatorio_coluna = lambda i: sum(p[i] for p in self.pontos)
        coordenadas_centroide = [obtem_somatorio_coluna(i)/len(self.pontos) for i in range(len(self.pontos[0]))] 
        return coordenadas_centroide

def kmeans(pontos, num_classes, criterio_parada=0.5, centros_iniciais=[]):
    centroides_iniciais = random.sample(pontos, num_classes) if not centros_iniciais else centros_iniciais
    # cria os clusters com apenas um ponto aleatório para depois ajusta-lo
    clusters = [Cluster([p]) for p in centroides_iniciais]
    iteracoes = 0
    while True and iteracoes < 100:
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
            break
    return clusters, iteracoes

def menor_distancia(x, pontos):
    return min([ed(x, xi) for xi in pontos if xi != x])

def kmeanspp(pontos, num_classes, criterio_parada=0.5):
    # referência: http://ilpubs.stanford.edu:8090/778/1/2006-13.pdf
    #1.a - Take one center ci chosen uniformly at random from X
    centroides = [random.choice(pontos)]
    #1.b - Take a new center ci choosing x \in X with probability D(x)^2/sum(x \in X)(D(x)^2)
    #1.c - Repeat Step 1b. until we have taken k centers altogether.
    for i in range(1, num_classes):
        centroide = None
        while centroide is None:
            centroide = random.choice(pontos)
            probabilidade = menor_distancia(centroide, pontos)/sum([menor_distancia(centroide, pontos) for xi in pontos])
            if random.random() < probabilidade*10:
                centroides.append(centroide)
            else:
                centroide = None
    # Proceed as with the standard k-means algorithm.
    return kmeans(pontos, num_classes, criterio_parada, centroides)

def teste_dataset(dataset, titulo):
    dataset = load_dataset(dataset)
    if len(dataset) > 100:
        np.random.shuffle(dataset)
        dataset = dataset[:100]
    pontos = [[float(linha[0]), float(linha[1])] for linha in dataset]
    num_classes, criterio_parada = 4, 0.01
    iteracoes_km = []
    iteracoes_kmpp = []
    for i in range(30):
        clusters, iteracoes = kmeans(pontos, num_classes, criterio_parada)
        iteracoes_km.append(iteracoes)
        clusters, iteracoes = kmeanspp(pontos, num_classes, criterio_parada)
        iteracoes_kmpp.append(iteracoes)
    fig, axes = plt.subplots(nrows=1, ncols=2)
    axes[0].boxplot(iteracoes_km, labels=['K-means'])
    axes[0].set_title(titulo)
    axes[1].boxplot(iteracoes_kmpp, labels=['K-means++'])
    axes[1].set_title(titulo)
    plt.show()

def main():
    teste_dataset('ruspini.txt', u'Ruspini')
    teste_dataset('user-identification-walking-activity.csv', u'User identification by walking activity')
    
    #cores = ['r', 'g', 'b', 'y']
    #formas = ['o', '*', '^']
    #coresxformas = [c+f for f in formas for c in cores]

    #for i,c in enumerate(clusters): 
    #    plt.plot([c.centroide[0]], [c.centroide[1]], coresxformas[i][0]+'+')
    #    for p in c.pontos:
    #        plt.plot([p[0]], [p[1]], coresxformas[i])
    #plt.show()

if __name__ == "__main__": 
    main()
