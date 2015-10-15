# encoding: utf-8

import time
from math import cos, sin,pi
import numpy as np
from numpy.random import rand
import matplotlib.pyplot as plt
from anneal import anneal
from differential_evolution import differential_evolution
from evolution_strategy import es

# metropolis = boltzmann

inf = float('inf')

def gi(x):
    return any([sin(2*pi*xi) + 0.5 <= 0 for xi in x])

def hj(x):
    return any([cos(2*pi*xj) + 0.5 == 0 for xj in x])

DADOS_EXECUCAO = []
ITERACOES = 0

def rastrigin(x):
    global DADOS_EXECUCAO
    global ITERACOES
    n = len(x)
    valor = 10*n + sum([x[i]**2 - 10*cos(2*pi*x[i]) for i in range(n)])
    DADOS_EXECUCAO.append(valor)
    ITERACOES += 1
    return valor

def anneal_teste20s(n):
    global DADOS_EXECUCAO
    global ITERACOES
    DADOS_EXECUCAO = []
    ITERACOES = 0
    x0 = rand(1,n)[0]
    r = anneal(rastrigin, 
            x0, 
            maxiter=inf,
            maxeval=inf,
            maxaccept=inf,
            feps=-inf,
            lower=-5.12,
            upper=5.12,
            T0=1e5,
            Tf=1e-10,
            learn_rate=0.995,
            full_output=True,
            disp=False,
            max_execution_time=20,
            schedule='boltzmann',
            )
    return r

def anneal_testeiteracoes(n):
    global DADOS_EXECUCAO
    global ITERACOES
    DADOS_EXECUCAO = []
    ITERACOES = 0
    x0 = rand(1,n)[0]
    return anneal(rastrigin,
            x0, 
            maxiter=1e4,
            maxeval=1e4,
            maxaccept=1e4,
            feps=-inf,
            lower=-5.12,
            upper=5.12,
            T0=1e5,
            Tf=1e-10,
            learn_rate=0.995,
            full_output=True,
            disp=False,
            schedule='boltzmann')

def de_teste20s(n):
    global DADOS_EXECUCAO
    global ITERACOES
    DADOS_EXECUCAO = []
    ITERACOES = 0
    return differential_evolution(rastrigin, [(-5.12, 5.12)]*n, maxiter=inf, tol=-inf, max_execution_time=20, popsize=20, recombination=0.5)

def de_testeiteracoes(n):
    global DADOS_EXECUCAO
    global ITERACOES
    DADOS_EXECUCAO = []
    ITERACOES = 0
    return differential_evolution(rastrigin, [(-5.12, 5.12)]*n, maxiter=10000, tol=-inf, popsize=20, recombination=0.5)

def es_teste20s(n):
    result = es(fitness=rastrigin, bounds_min=-5.12, bounds_max=5.12, mu=20, lambda_=5, dimension=n, sigma_init=20, max_execution_time=20)
    return result

def es_testeiteracoes(n):
    result = es(fitness=rastrigin, bounds_min=-5.12, bounds_max=5.12, mu=20, lambda_=5, dimension=n, sigma_init=20, maxiter=10000)
    return result

def main():
    resultados_tempo = []
    for i in range(100):
        for dim in (3, 5, 10):
            #simulated annealing - critério de iteracoes
            resultado = anneal_testeiteracoes(dim)
            DADOS_EXECUCAO.append(rastrigin(resultado[0]))
            plt.plot(range(0, len(DADOS_EXECUCAO)), DADOS_EXECUCAO, 'r-')
            plt.savefig('p2-sa-ci-{}d-n{}.png'.format(dim, str(i+1).rjust(3, '0')))
            plt.clf()

            #differential evolution - critério de iteracoes
            resultado = de_testeiteracoes(dim)
            DADOS_EXECUCAO.append(rastrigin(resultado.x))
            plt.plot(range(0, len(DADOS_EXECUCAO[:1500])), DADOS_EXECUCAO[:1500], 'b-')
            plt.savefig('p2-de-ci-{}d-n{}.png'.format(dim, str(i+1).rjust(3, '0')))
            plt.clf()

            # evolution strategy - critério de iterações
            resultado = es_testeiteracoes(dim)
            plt.plot(range(len(resultado[1])), resultado[1], 'g-')
            plt.savefig('p2-es-ci-{}d-n{}.png'.format(dim, str(i+1).rjust(3,'0')))
            plt.clf()

            #simulated annealing - critério de tempo
            resultado = anneal_teste20s(dim)
            DADOS_EXECUCAO.append(rastrigin(resultado[0]))
            plt.plot(range(0, len(DADOS_EXECUCAO)), DADOS_EXECUCAO, 'r-')
            plt.savefig('p2-sa-ct-{}d-n{}.png'.format(dim, str(i+1).rjust(3, '0')))
            plt.clf()
            if dim == 3:
                resultados_tempo.append(('sa', resultado[0]))

            #differential evolution - critério de tempo
            resultado = de_teste20s(dim)
            DADOS_EXECUCAO.append(rastrigin(resultado.x))
            plt.plot(range(0, len(DADOS_EXECUCAO[:1500])), DADOS_EXECUCAO[:1500], 'b-')
            if dim == 3:
                resultados_tempo.append(('de', resultado.x))
            plt.savefig('p2-de-ct-{}d-n{}.png'.format(dim, str(i+1).rjust(3, '0')))
            plt.clf()

            # evolution strategy - critério de tempo 
            resultado = es_teste20s(dim)
            plt.plot(range(len(resultado[1][:100])), resultado[1][:100])
            plt.savefig('p2-es-ct-{}d-n{}.png'.format(dim, str(i+1).rjust(3,'0')))
            plt.clf()
            if dim == 3:
                resultados_tempo.append(('es', resultado[0][2]))

    media_de = np.mean([abs(x[1]) for x in resultados_tempo if x[0] == 'de'])
    std_de = np.std([x[1] for x in resultados_tempo if x[0] == 'de'])
    minimo_de = np.min([abs(x[1]) for x in resultados_tempo if x[0] == 'de'])

    media_sa = np.mean([abs(x[1]) for x in resultados_tempo if x[0] == 'sa'])
    std_sa = np.std([x[1] for x in resultados_tempo if x[0] == 'sa'])
    minimo_sa = np.min([abs(x[1]) for x in resultados_tempo if x[0] == 'sa'])

    media_es = np.mean([abs(x[1]) for x in resultados_tempo if x[0] == 'es'])
    std_es = np.std([x[1] for x in resultados_tempo if x[0] == 'es'])
    minimo_es = np.min([abs(x[1]) for x in resultados_tempo if x[0] == 'es'])

    print "DE: media:",media_de, " - desvio padrão: ",std_de, "- minimo: ", minimo_de
    print "SA: media:",media_sa, " - desvio padrão: ",std_sa, "- minimo: ", minimo_sa
    print "ES: media:",media_es, " - desvio padrão: ",std_es, "- minimo: ", minimo_es

if __name__=='__main__':
    main()
