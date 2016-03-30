# encoding: utf-8
import sys
import random
import copy
import math
import jellyfish
import numpy
from collections import namedtuple, OrderedDict as od

"""
ToDo:
    - Cáculo de fitness de árvores incompletas: implementar metodo num_folhas_faltantes em Arvore
"""

Formiga = namedtuple('Formiga', ['local', 'caminho', 'custo'])
numeros_reais = [0.1, 0.3, 0.5, 0.7, 0.9]
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

variaveis, dataset = load_dataset()

def custo(funcao): #o original eh fitness. custo = 1-fitness
    resultado = dict(true_p=0, false_p=0, false_n=0)
    for linha in dataset:
        val = funcao(**linha)
        if val >= 0.95:
            if linha['match']:
                resultado['true_p'] += 1
            else:
                resultado['false_p'] += 1
        else:
            if linha['match']:
                resultado['false_n'] += 1
            else:
                pass #verdadeiro-negativo -- n interessa p nos
    denominador_precisao = (resultado['true_p']+resultado['false_p'])
    precisao = float(resultado['true_p'])/denominador_precisao if denominador_precisao else 0
    denominador_recall = (resultado['true_p']+resultado['false_n'])
    recall = float(resultado['true_p'])/denominador_recall if denominador_recall else 0
    f1 = 2*(precisao*recall)/(precisao+recall) if precisao+recall else 0
    return 1-f1

class Arvore(object):
    def __init__(self, op, left=None, right=None):
        self.op = op
        self.left = left
        self.right = right
    
    def run(self, **kwargs):
        if type(self.op) in (str, unicode) and self.op not in operadores.keys():
            return kwargs[self.op]
        if type(self.op) in (int, float):
            return self.op
        left, right = self.left, self.right
        if left is None:
            left = elementos_neutros[self.op]
        if type(left) == Arvore:
            left = self.left.run(**kwargs)
        if right is None:
            right = elementos_neutros[self.op]
        if type(right) == Arvore:
            right = self.right.run(**kwargs)

        if type(left) in (str, unicode):
            left = kwargs[left]
        if type(right) in (str, unicode):
            right = kwargs[right]
        try:
            return operadores[self.op](left, right)
        except TypeError:
            import pdb;pdb.set_trace()
        except ZeroDivisionError:
            return 0

    __call__ = run

    def __str__(self):
        if self.op in operadores.keys():
            right = str(self.right) if self.right is not None else elementos_neutros[self.op]
            left = str(self.left) if self.left is not None else elementos_neutros[self.op]
            return '({op} {left} {right})'.format(op=self.op, left=self.left, right=self.right)
        return str(self.op)
    
    def to_path(self):
        if self.op in operadores.keys():
            right = self.right.to_path() if self.right is not None else [elementos_neutros[self.op]]
            left = self.left.to_path() if self.left is not None else [elementos_neutros[self.op]]
            return [self.op]+left+right
        return [self.op]

def inicializa_grafo():
    vertices = numeros_reais + operadores.keys() + variaveis
    grafo = dict()
    for v1 in vertices:
        grafo[v1] = dict()
        for v2 in vertices:
            grafo[v1][v2] = random.uniform(1,5)
    return grafo

def inicializa_feromonio(grafo, tau0):
    feromonio = dict()
    for origem in grafo.keys():
        feromonio[origem] = dict()
        for destino in grafo.keys():
            feromonio[origem][destino] = tau0
    return feromonio

def inicializa_formigas(qtd):
    for q in xrange(qtd):
        caminho = [random.choice(operadores.keys())]
        _custo = custo(caminho_para_arvore(copy.copy(caminho)))
        yield Formiga(local=caminho[0], caminho=caminho, custo=_custo)

def obter_solucoes(formigas, feromonio, grafo, params):

    novas_formigas = []
    for formiga in formigas:
        formiga = poda(formiga)
        caminho_original = copy.copy(formiga.caminho)
        custo_original = formiga.custo
        for passo in range(params['max_passos_formiga']):
            vertice = escolher_vertice(formiga, feromonio, grafo, params)
            if vertice:
                formiga = Formiga(local=vertice, caminho=formiga.caminho+[vertice], custo=custo(caminho_para_arvore(formiga.caminho+[vertice])))
                feromonio = atualiza_feromonio_local([formiga], feromonio, grafo, params)
        if custo_original > formiga.custo:
            novas_formigas.append(formiga)
        else:
            novas_formigas.append(Formiga(local=caminho_original[-1], caminho=caminho_original, custo=custo_original))
    formigas = novas_formigas
    return formigas, feromonio

def poda(formiga):
    caminho = copy.copy(formiga.caminho)
    caminho_otimizado = caminho_para_arvore(caminho).to_path()
    if caminho_otimizado[-1] not in operadores.keys():
        caminho_otimizado = caminho_otimizado[:-1]
    return Formiga(local=caminho_otimizado[-1], caminho=copy.copy(caminho_otimizado), custo=formiga.custo)

def atualiza_feromonio_local(formigas, feromonio, grafo, params):
    caminhos = [(formiga.caminho[-2], formiga.caminho[-1]) for formiga in formigas if len(formiga.caminho) > 1]
    try:
        sumdelta_tau_ijk = sum((params['Q']/grafo[origem][destino]) for origem,destino in caminhos)
    except KeyError:
        import pdb;pdb.set_trace()
    for origem,destino in caminhos:
        val = (1 - params['rho'])*feromonio[origem][destino] + sumdelta_tau_ijk
        if val in (float('nan'), float('inf'), float('-inf')):
            import pdb;pdb.set_trace()
        feromonio[origem][destino] = (1 - params['rho'])*feromonio[origem][destino] + sumdelta_tau_ijk
    return feromonio

def escolher_vertice(formiga, feromonio, grafo, params):
    if len(formiga.caminho) < 3:
        return escolhe_vertice_aleatoriamente_dentro_distribuicao_poisson()
    origem = formiga.local
    vertices = grafo.keys()
    random.shuffle(vertices)
    for v in vertices:
        sum_tau_ij_eta_ij = sum(math.pow(feromonio[o][v], params['alpha'])*
                                math.pow(1/grafo[o][v], params['beta'])
                                for o in grafo.keys())
        p_ij_k  = math.pow(feromonio[origem][v], params['alpha'])*math.pow((1/grafo[origem][v]), params['beta'])
        p_ij_k /= sum_tau_ij_eta_ij
        if p_ij_k > random.random():
            return v
    #import pdb;pdb.set_trace()
    return escolhe_vertice_aleatoriamente_dentro_distribuicao_poisson()

def escolhe_vertice_aleatoriamente_dentro_distribuicao_poisson():
    return (operadores.keys()+variaveis)[numpy.random.poisson(3)]

def caminho_para_arvore(caminho, arvore=None):
    # [+, 1, -, 3] => [+, 1, [-, 3, 0]]
    if not arvore and caminho:
        if caminho[0] in operadores.keys():
            arvore = Arvore(caminho.pop(0))
        else:
            arvore = Arvore(caminho.pop(0))
            return arvore
    if type(arvore) == Arvore:
        if arvore.left is None:
            arvore.left = caminho_para_arvore(caminho, arvore.left)
        if arvore.right is None:
            arvore.right = caminho_para_arvore(caminho, arvore.right)
    return arvore

def melhor_formiga(formigas):
    return sorted([(f.custo, f) for f in formigas])[1]

def main():
    #params
    tau0 = 0.1
    num_formigas = 20
    max_passos_formiga = 10
    max_geracoes = 20
    rho = 0.5 #taxa de evaporacao
    phi = 0.9 #taxa de decaimento do feromonio
    Q = 1.0 # constante usada no cálculo deltaTau_ij
    alpha = 1
    beta = 4
    params = locals()

    grafo = inicializa_grafo()
    formigas = list(inicializa_formigas(num_formigas))
    feromonio = inicializa_feromonio(grafo, tau0)
    for g in range(max_geracoes):
        formigas, feromonio = obter_solucoes(formigas, feromonio, grafo, params)
        melhor = melhor_formiga(formigas)
        print melhor
        #import pdb;pdb.set_trace()

def simpletest():
    funcao = caminho_para_arvore(['+', '-', -23.40821450189093, '+', 'suburb',
        17.87985586929176, '*', '*', '*', 'suburb', '+', 'postcode', '+',
        'state', 2.152285332089705, '-', '*', 'soc_sec_id', 'date_of_birth',
        13.450478384019448, '-', '-', 'given_name', 'surname', '*', 'state',
        'given_name'])
    print str(funcao)
    print custo(funcao)

if __name__ == '__main__':
    if 'test' in sys.argv:
        simpletest()
    else:
        main()
