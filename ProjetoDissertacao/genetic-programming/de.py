# encoding: utf-8
import sys
import time
import copy
import random
import datetime
import json
import multiprocessing
from jellyfish import jaro_winkler

DATASET = []

def fitness(individuo):
    individuo= individuo['individuo']
    global DATASET
    if not DATASET:
        linhas = unicode(open('dataset.csv').read()).split('\n')
        header = [l.strip() for l in linhas[0].split(',')]
        DATASET = [dict(zip(header, [l.strip() for l in linha.strip().split(',')])) for linha in linhas[1:] if linha]
    verdadeiro_positivo = 0
    verdadeiro_negativo = 0
    falso_positivo = 0
    falso_negativo = 0
    for l1 in xrange(len(DATASET)):
        for l2 in range(l1+1, len(DATASET)):
            linha1, linha2 = DATASET[l1], DATASET[l2]
            if linha1 == linha2:
                continue
            resultado = calc_score(linha1, linha2, individuo)
            if mesmo_registro(linha1, linha2):
                if resultado <= 0.95:
                    falso_negativo += 1
                else:
                    verdadeiro_positivo += 1
            else:
                if resultado <= 0.95:
                    verdadeiro_negativo += 1
                else:
                    falso_positivo += 1
    try:
        precisao = verdadeiro_positivo/float(verdadeiro_positivo+falso_positivo)
        recall = verdadeiro_positivo/float(verdadeiro_positivo+falso_negativo)
        f1 = (2*precisao*recall)/(precisao+recall)
    except ZeroDivisionError:
        f1 = 0
    print datetime.datetime.now(), f1
    return dict(individuo=individuo, fitness=f1)

def calc_score(linha1, linha2, coeficientes):
    return sum([coeficientes[i]*jaro_winkler(linha1.values()[i], linha2.values()[i]) for i in range(len(coeficientes))])

def mesmo_registro(reg1, reg2):
    return reg1['rec_id'].split('-')[1] == reg2['rec_id'].split('-')[1]

"""
Representação do indivíduo:
    Vetor de números reais com N posições, sendo N a quantidade de atributos da
    base de dados. Cada atributo desse será multiplicado com o resultado da
    função de comparação (jaro_winkler) e o resultado do vetor será somado
    depois. O DE só vai escolher os pesos de cada atributo.

    Ex: Considere um par de registros duplicados com nome, sobrenome, e
    telefone e um limiar de 0.95 para considerar um par.

    reg1: Herbert, Amaral, 3222 3360
    reg1: Herberth, Silva, 99241 7268
    --------------------------------
    jw  : 0.975, 0.456, 0.531
    pesos: 1, 0 , 0
    score: 0.975*1 + 0.456*0 + 0.531*0 = 0.975
"""

def init_pop(qtd, attrs, multi, calc_fitness=True):
    pop = [{'individuo': [random.uniform(0,2) for a in attrs], 'fitness':None} for i in range(qtd)]
    if calc_fitness:
        return calcula_fitness_pop(pop, multi)
    return pop

POOL = None
def calcula_fitness_pop(pop, multi):
    global POOL
    a_calcular = []
    for individuo in pop:
        if individuo['fitness'] is None:
            a_calcular.append(individuo)
    individuos = [i for i in pop if i['fitness'] is not None]
    if multi:
        if not POOL:
            POOL = multiprocessing.Pool(multiprocessing.cpu_count())
        individuos.extend(POOL.map(fitness, a_calcular))
    else:
        individuos.extend([fitness(a) for a in a_calcular])
    individuos = sorted(individuos, key=lambda x:-x['fitness'])
    return individuos

def evolve(pop, multi, num_geracoes=20):
    nu = 0.5
    n = len(pop[0]['individuo'])
    C = 0.75
    for g in range(num_geracoes): #critério de parada
        nova_populacao = []
        for i,agente in enumerate(pop):
            x_tr1, x_tr2, x_tr3 = random.sample(pop, 3)
            delta = random.randint(0, n)
            novo_individuo = []
            for j in range(n):
                if random.random() < C or j == delta:
                    novo_individuo.append(x_tr1['individuo'][j] + nu*(x_tr2['individuo'][j] - x_tr3['individuo'][j]))
                else:
                    novo_individuo.append(agente['individuo'][j])
            nova_populacao.append({'individuo': novo_individuo, 'fitness': None})
        nova_populacao = calcula_fitness_pop(nova_populacao, multi)
        proxima_geracao = []
        for i in range(len(nova_populacao)):
            if nova_populacao[i]['fitness'] < pop[i]['fitness']:
                proxima_geracao.append(pop[i])
            else:
                proxima_geracao.append(nova_populacao[i])
        pop = proxima_geracao
        pop = sorted(pop, key=lambda x:-x['fitness'])
        print u'\nMelhor fitness da geração ',(g+1), pop[0]['fitness']
        print u'\nMelhor indivíduo:', pop[0]['individuo']
    return sorted(pop)[-1]

def de(multi=True):
    attrs=['given_name','surname','street_number','address_1','address_2','suburb','postcode','state','date_of_birth','soc_sec_id']
    pop = init_pop(20, attrs, multi)
    melhor = evolve(pop, multi, num_geracoes=100)
    print melhor

if __name__ == '__main__':
    de(multi=True)
