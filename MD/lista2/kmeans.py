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
            print "Novo centroide:", self.centroide
            return ed(self.centroide_anterior, self.centroide)
        else: #caso o centróide não tenha nenhum ponto próximo...
            self.ficou_sem_ponto = True
            return 1 #... faz com que ele seja movido através de uma pertubação

    def calcula_centroide(self):
        obtem_somatorio_coluna = lambda i: sum(p[i] for p in self.pontos)
        coordenadas_centroide = [obtem_somatorio_coluna(i)/len(self.pontos) for i in range(len(self.pontos[0]))] 
        return coordenadas_centroide

def kmeans(pontos, num_classes, criterio_parada=0.5, centros_iniciais=[], max_iteracoes=100):
    centroides_iniciais = random.sample(pontos, num_classes) if not centros_iniciais else centros_iniciais
    print "Centróides iniciais: ", centros_iniciais
    # cria os clusters com apenas um ponto aleatório para depois ajusta-lo
    clusters = [Cluster([p]) for p in centroides_iniciais]
    iteracoes = 0
    while True and iteracoes < max_iteracoes:
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
