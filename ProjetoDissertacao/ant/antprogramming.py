# encoding: utf-8
import random
import jellyfish
from collections import namedtuple, OrderedDict as od

"""
ToDo:
    - Importar funções de fitness e interpretação de árvores
    - Cáculo de fitness de árvores incompletas: completar com elementos neutros (0 para add/sub, 1 para mul/div)
"""

Formiga = namedtuple('Formiga', ['local', 'caminho', 'fitness'])
numeros_reais = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
operadores = {'+': lambda x,y: x+y,
              '-': lambda x,y: x-y,
              '*': lambda x,y: x*y, 
              '/': lambda x,y: x/y}
elementos_neutros = {'+': 0, '-':0, '*':1, '/':1}

def load_dataset(filename='out.csv'):
    content = [map(lambda x: unicode(x).strip(), linha.split(',')) for linha in open('out.csv', 'r').read().split('\n') if linha]
    header = content[0]
    content = content[1:]
    comparacoes = []
    for linha1 in content:
        for linha2 in content:
            if linha1 == linha2:
                continue
            comp = od(rec1=linha1[0].split('-')[1], rec2=linha2[0].split('-')[1])
            for i, field in enumerate(header[1:]):
                comp[field] = jellyfish.jaro_winkler(linha1[i+1], linha2[i+1])
            comp['match'] = comp['rec1']==comp['rec2']
            comparacoes.append(comp)
    return header[1:], comparacoes

variables, dataset = load_dataset()

def custo(funcao): #o original eh fitness. custo = 1-fitness
    resultado = dict(true_p=0, false_p=0, false_n=0)
    for linha in dataset:
        val = funcao(**linha)
        if val > 0.95:
            if linha['match']:
                resultado['true_p'] += 1
            else:
                resultado['false_p'] += 1
        else:
            if linha['match']:
                resultado['false_n'] += 1
            else:
                pass #verdadeiro-negativo -- n interessa p nos
    precisao = float(resultado['true_p'])/(resultado['true_p']+resultado['false_p'])
    recall = float(resultado['true_p'])/(resultado['true_p']+resultado['false_n'])
    f1 = 2*(precisao*recall)/(precisao+recall)
    return 1-f1

class Tree(object):
    def __init__(self, op, left=None, right=None):
        self.op = op
        self.left = left
        self.right = right
    
    def run(self, **kwargs):
        if type(self.op) in (str, unicode) and self.op not in operadores.keys():
            return kwargs[self.op]
        left, right = self.left, self.right
        if left is None:
            left = elementos_neutros[self.op]
        if type(left) == Tree:
            left = self.left.run(**kwargs)
        if right is None:
            right = elementos_neutros[self.op]
        if type(right) == Tree:
            right = self.right.run(**kwargs)

        if type(left) == str:
            left = kwargs[left]
        if type(right) == str:
            right = kwargs[right]
        return operadores[self.op](left, right)

    __call__ = run

def inicializa_grafo():
    vertices = numeros_reais + operadores.keys() + variables
    grafo = dict()
    for v in vertices:
        grafo[v] = vertices
    return grafo

def inicializa_feromonio(grafo, tau0):
    feromonio = dict()
    for origem in grafo.keys():
        feromonio[origem] = dict()
        for destino in grafo.keys():
            feromonio[origem][destino] = tau0
    return feromonio

def inicializa_formigas(qtd):
    return [Formiga(local='', caminho=[random.choice(operadores.keys())], fitness=0) for n in range(qtd)]

def obter_solucoes(formigas, feromonio, grafo, max_passos_formiga):
    passo = 0
    while passo < max_passos_formiga:
        passo += 1
        novas_formigas = []
        for formiga in formigas:
            vertice = escolher_vertice(formiga)
            caminho = formiga.caminho+[vertice]
            arvore = caminho_para_arvore(caminho)
            novas_formigas.append(Formiga(local=vertice, caminho=caminho, fitness=fitness(arvore)))

def caminho_para_arvore(caminho, arvore=None):
    # [+, 1, -, 3] => [+, 1, [-, 3, 0]]
    if not arvore and caminho:
        arvore = Tree(caminho.pop(0))
    if type(arvore) == Tree:
        if arvore.left is None:
            arvore.left = caminho_para_arvore(caminho, arvore.left)
        if arvore.right is None:
            arvore.right = caminho_para_arvore(caminho, arvore.right)
    return arvore

def main():
    #params
    tau0 = 0.1
    num_formigas = 20
    max_passos_formiga = 10
    max_geracoes = 20
    rho = 0.5 #taxa de evaporacao
    params = locals()

    grafo_percurso = inicializa_grafo()
    formigas = inicializa_formigas(num_formigas)
    feromonio = inicializa_feromonio(grafo, tau0)
    for g in range(max_geracoes):
        formigas, feromonio = obter_solucoes(formigas, feromonio, grafo)
        print melhor_formiga(formigas).caminho

funcao = caminho_para_arvore(['+', 'given_name', 'surname'])
print custo(funcao)
