# encoding: utf-8
import sys
import math
import random
from collections import namedtuple
sort = lambda x: tuple(sorted(x))

#random.seed(0) #deixa determinístico

#cidades = {
#    'moc':{ 'boc': 47.5, 'pir': 171, 'mir': 67.1, 'jnb': 134, },
#    'mir':{ 'jan': 103, 'moc': 67.1, },
#    'jan':{ 'mng': 107, 'mir': 103, },
#    'jnb':{ 'moc': 134, 'mng': 145, },
#    'mng':{ 'jnb': 145, 'jan': 107 },
#    'pir':{ 'cor': 140, 'moc': 171 },
#    'boc':{ 'cor': 167, 'moc': 47.5, 'dia': 181 },
#    'dia':{ 'cur': 129, 'boc': 181 },
#    'cur':{ 'cor': 47.4, 'dia': 129, 'bhz': 172, },
#    'cor':{ 'cur': 47.4 },
#    'bhz' :{ 'cur': 172 },
#}

Formiga = namedtuple('Formiga', ['cidade_atual', 'caminho_percorrido', 'custo'])
Aresta = namedtuple('Aresta', ['origem', 'destino'])

def distancia_euclidiana(a, b): # a e b são coordenadas, tipo a = (1, 5)
    return math.sqrt(math.pow(sum([a[i]-b[i] for i in range(len(a))]), 2)) or 1e-5

def load_data(arquivo='d1291.data'):
    matrix = dict()
    content = [map(float, s.split(' ')) for s in open(arquivo, 'r').read().split('\n') if s!='']
    for linha1 in content:
        cidade1 = linha1[0]
        matrix[cidade1] = {}
        for linha2 in content:
            if linha1 == linha2:
                continue
            cidade2 = linha2[0]
            matrix[cidade1][cidade2] = distancia_euclidiana(linha1[1:], linha2[1:])
    return matrix

cidades = load_data()

# objetivo: encontrar um caminho de manga a BH
def custo(caminho):
        """
        Exemplo de caminho: ['moc', 'boc', 'cor', 'cur', 'bhz']
        """
        arestas = [Aresta(origem=a[0], destino=a[1]) for a in zip(caminho[0:-1], caminho[1:])]
        distancia = 0
        for aresta in arestas:
            try:
                distancia += cidades[aresta.origem][aresta.destino]
            except KeyError: 
                print u'Caminho não existe: ', aresta
                return float('inf')
        return distancia

def inicializa_formigas(qtd, partida):
    return [Formiga(cidade_atual=partida, caminho_percorrido=[partida], custo=0) for i in range(qtd)]

def melhor(formigas):
    melhores = filter(lambda f: f.custo != 0, sorted(formigas, key=lambda f: f.custo, reverse=True))
    if melhores:
        return melhores[0]

def busca_solucao(formigas, feromonio_arestas, params):
    max_it = len(cidades)*2
    i = 0
    while i<max_it:
        i+=1
        novas_formigas = []
        for formiga in formigas:
            while len(formiga.caminho_percorrido) != len(cidades):
                proxima_cidade = obter_proxima_cidade(formiga, feromonio_arestas, params)
                formiga.caminho_percorrido.append(proxima_cidade)
            novas_formigas.append(Formiga(cidade_atual=proxima_cidade, caminho_percorrido=formiga.caminho_percorrido, custo=custo(formiga.caminho_percorrido)))
        formigas = novas_formigas
        feromonio_arestas = atualiza_feromonio_local(formigas, feromonio_arestas, params)
        if filter(lambda f, params=params: f.cidade_atual == params['chegada'], formigas): #achou solução
            break
    feromonio_arestas = atualiza_feromonio_global(formigas, feromonio_arestas, params)
    return formigas, feromonio_arestas

def penaliza_rota(aresta, feromonio_arestas):
    feromonio_arestas[sort(aresta)] = 1e-8
    return feromonio_arestas

def atualiza_feromonio_global(formigas, feromonio_arestas, params):
    melhor_formiga = melhor(formigas)
    if not melhor_formiga:
        return feromonio_arestas
    caminho = melhor_formiga.caminho_percorrido
    arestas_melhor_formiga  = [Aresta(origem=a[0], destino=a[1]) for a in zip(caminho[0:-1], caminho[1:])]

    delta_t = 1/melhor_formiga.custo
    for aresta in arestas_melhor_formiga:
        feromonio_arestas[sort(aresta)] = (1-params['rho'])*feromonio_arestas[sort(aresta)] + params['rho']*delta_t
    return feromonio_arestas

def atualiza_feromonio_local(formigas, feromonio_arestas, params):
    for formiga in formigas:
        if len(formiga.caminho_percorrido) == 1:
            #algumas formigas podem ser reiniciadas no passo anterior
            continue
        origem = formiga.caminho_percorrido[-2]
        destino = formiga.caminho_percorrido[-1]
        #as
        possiveis_cidades = cidades[origem].keys()
        for p in possiveis_cidades:
            delta = 0 if p != destino else params['Q']/(1.0/cidades[origem][p])
            aresta = sort((origem, p))
            feromonio_arestas[aresta] =  (1-params['rho'])*feromonio_arestas[aresta] + delta

        #acs
        aresta = sort((origem, destino))
        feromonio_arestas[aresta] = (1-params['phi'])*feromonio_arestas[aresta]+params['phi']*params['c']

    return feromonio_arestas

def obter_proxima_cidade(formiga, feromonio_arestas, params):
    possiveis_cidades = list(set(cidades[formiga.cidade_atual].keys())-set(formiga.caminho_percorrido))
    random.shuffle(possiveis_cidades)
    cidade_escolhida = ''
    maior_probabilidade = 0
    denominador = sum([math.pow(1.0/cidades[formiga.cidade_atual][p],params['alpha'])*math.pow(feromonio_arestas[sort((formiga.cidade_atual, p))], params['beta']) for p in possiveis_cidades])
    if not possiveis_cidades:
        return cidade_escolhida
    rating_cidades = dict()
    for p in possiveis_cidades:
        desejabilidade = math.pow(1.0/cidades[formiga.cidade_atual][p], params['beta'])
        aresta = sort((formiga.cidade_atual, p))
        feromonio_xy =  math.pow(feromonio_arestas[aresta], params['alpha'])
        pxy = feromonio_xy*desejabilidade
        rating_cidades[p] = pxy
    
    #if len(formiga.caminho_percorrido) > 1:
    #    import pdb;pdb.set_trace()
    if random.random() < params['q0']: # destino = argmax pxy
        max_rating = max(rating_cidades.values())
        pos_max_rating = rating_cidades.values().index(max_rating)
        cidade_escolhida = rating_cidades.keys()[pos_max_rating]
    else:
        sum_pxy = sum(map(lambda r: r[1], rating_cidades.items()))
        maior_score = 0
        cidade_maior_score = ''
        for p in possiveis_cidades:
            score = rating_cidades[p]/sum_pxy
            if score > maior_score:
                maior_score = score
                cidade_maior_score = p
        cidade_escolhida = cidade_maior_score
    return cidade_escolhida

def inicializa_feromonio(c):
    feromonio_arestas = dict()
    for c1 in cidades.keys():
        for c2 in cidades[c1].keys():
            feromonio_arestas[sort((c1,c2))] = c
    return feromonio_arestas

def print_feromonio(feromonio):
    ordenado = sorted(feromonio.items(), key= lambda item: item[1])
    for o in ordenado:
        print '{} <-> {} : {}'.format(o[0][0], o[0][1], o[1])

def main():
    c = 0.1 #feromonio padrão
    Q = 1
    q0 = 0.5  #constante usada na atualização de feromonio
    num_formigas = 10
    alpha = 3 # influência de caminho -- se for 0 usa a estratégia gulosa de sempre escolher o menor caminho
    beta = 1 # influência de feromônio -- se for 0 sempre vai pro caminho que tem mais feromônio (o que pode levar a uma convergência prematura)
    rho = 0.001 #coeficiente de evaporação
    phi = 0.5 #taxa de decaimento do feromonio
    partida = 1.0
    chegada = 1291.0
    num_iteracoes = 10 
    params = locals()
    feromonio_arestas = inicializa_feromonio(c)

    for iteracao in range(num_iteracoes):
        formigas = inicializa_formigas(num_formigas, partida)
        formigas, feromonio_arestas = busca_solucao(formigas, feromonio_arestas, params)
        validas =  filter(lambda f, params=params: f.cidade_atual == params['chegada'], formigas)
        melhor_formiga = melhor(validas)
        if melhor_formiga:
            import pdb;pdb.set_trace()
            print 'Melhor formiga da iteracao {}: {}'.format(iteracao+1, melhor_formiga.custo)
        else:
            print 'Sem soluções factíveis na iteração', iteracao+1

main()
