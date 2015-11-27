# encoding: utf-8
"""
Análise dos dados coletados
"""
import os
import json
import numpy as np
from collections import OrderedDict
from itertools import combinations
from scipy.stats import levene, kstest, normaltest, shapiro, anderson, ranksums
from scipy.stats.mstats import kruskalwallis
from main import FUNCOES, DATASETS

# carrega os dados
DADOS = []
for i in range(100):
    filename = 'iteracao-{num}.json'.format(num=str(i).rjust(3, '0'))
    if os.path.exists(filename):
        DADOS.extend(json.loads(open(filename).read()))

DADOS = np.array(DADOS)
def teste_normalidade(atributo):
    for f in FUNCOES:
        for d in DATASETS:
            dados = [i[atributo] for i in DADOS if i['dataset_file'] == d and i['function_path'] == f]
            s = shapiro(dados)[1]
            k = kstest(dados, 'norm')[1]
            n = normaltest(dados)[1]
            print s > 0.05, f, d, '- Shapiro' 
            print k > 0.05, f, d, '- Kolmogorov-Smirnov' 
            print n > 0.05, f, d, '- Normaltest' 

def calc_normalidade():
    print u"Analise de normalidade de tempo de teste"
    teste_normalidade('tteste')
    print '-'*100
    print u"Analise de normalidade da precisao"
    teste_normalidade('precisao')
    print '-'*100
    print u"Analise de normalidade do tempo de treinamento"
    teste_normalidade('ttreinamento')
    print '-'*100

def calc_ranksum():
    atributos = ['tteste', 'ttreinamento', 'precisao']
    for dataset in DATASETS:
        for atributo in atributos:
            for f1,f2 in combinations(FUNCOES, 2):
                d1 = np.array([i[atributo] for i in DADOS if i['dataset_file'] == dataset and i['function_path'] == f1])
                d2 = np.array([i[atributo] for i in DADOS if i['dataset_file'] == dataset and i['function_path'] == f2])
                print ','.join([str(s) for s in [dataset,atributo,f1,f2,ranksums(d1,d2)[0]]])

def calc_mediana():
    atributos = ['tteste', 'ttreinamento', 'precisao']
    for dataset in DATASETS:
        for atributo in atributos:
            for f1,f2 in combinations(FUNCOES, 2):
                d1 = np.array([i[atributo] for i in DADOS if i['dataset_file'] == dataset and i['function_path'] == f1])
                d2 = np.array([i[atributo] for i in DADOS if i['dataset_file'] == dataset and i['function_path'] == f2])
                print ','.join([str(s) for s in [dataset,atributo,f1,f2,np.median(d1),np.median(d2)]])

print teste_normalidade('precisao')
