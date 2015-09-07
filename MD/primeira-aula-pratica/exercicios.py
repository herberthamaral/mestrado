#!/usr/bin/env python
# encoding: utf-8
from __future__ import print_function
import sys
from collections import OrderedDict
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr, spearmanr
from chauvenet import chauvenet

def load_dataset(filename):
    dataset = open(filename, 'r').read().split('\n')
    dataset = [[dado.strip() for indice, dado in enumerate(linha.split(','))] for linha in dataset if linha]
    dataset = np.array(dataset)
    return dataset

def save_dataset(dataset, filename):
    conteudo = '\n'.join([','.join([str(i) for i in linha]) for linha in dataset])
    with file(filename, 'w') as fp:
        fp.write(conteudo)

correlacoes = [(0,1), (0,2), (0,3), (1,2), (1,3), (2,3)]
correlacoes_labels = ['altura sepal', 'largura sepal', 'altura petal', 'largura petal']

# Gráfico com os dados ordenados
def exercicio23c():
    iris = load_dataset('iris.data')
    for i, c in enumerate(correlacoes_labels):
        qtd = len([x for x in chauvenet(iris.T[i].astype(float)) if not x])
        if qtd > 0:
            pos = [l for l in chauvenet(iris.T[i].astype(float))].index(False)
            print("--Outlier na posição ", pos)
        print("Num outliers (utilizando o critério de Chauvenet) em {}: {}".format(c, qtd))
    for i,c in enumerate(correlacoes_labels):
        plt.plot(range(len(iris.T[i])), sorted(iris.T[i]), 'ro')
        plt.title('{}'.format(correlacoes_labels[i]))
        plt.show()

def exercicio23d():
    iris = load_dataset('iris.data')
    for c in correlacoes:
        p = pearsonr(iris.T[c[0]].astype(float), iris.T[c[1]].astype(float))[0]
        correlacao_grau = 'baixa' if abs(p) < 0.6 else 'alta'
        correlacao_tipo = 'inversamente proporcional' if p < 0 else 'diretamente proporcional'
        print("Correlação linear entre {0} e {1}: {2}, {3} e {4}".format(correlacoes_labels[c[0]], correlacoes_labels[c[1]], p, correlacao_grau, correlacao_tipo))

    # Analisando os gráficos anteriores, nota-se que as funções não são exatamente lineares.
    # por este motivo estou usando a correlação de spearman também
    print("\n\n\n\n\n--------------------------------%<-------------------------------\n\n\n\n\n")
    for c in correlacoes:
        p = spearmanr(iris.T[c[0]].astype(float), iris.T[c[1]].astype(float))[0]
        correlacao_grau = 'baixa' if abs(p) < 0.6 else 'alta'
        correlacao_tipo = 'inversamente proporcional' if p < 0 else 'diretamente proporcional'
        print("Correlação monotônica entre {0} e {1}: {2}, {3} e {4}".format(correlacoes_labels[c[0]], correlacoes_labels[c[1]], p, correlacao_grau, correlacao_tipo))


def exercicio23b():
    iris = load_dataset('iris.data')
    plt.hist(iris.T[0].astype(float))
    plt.xlabel('Altura sepal em cm')
    plt.ylabel('Frequencia')
    plt.show()

    plt.hist(iris.T[1].astype(float))
    plt.xlabel('Largura sepal em cm')
    plt.ylabel('Frequencia')
    plt.show()

    plt.hist(iris.T[2].astype(float))
    plt.xlabel('Altura petal em cm')
    plt.ylabel('Frequencia')
    plt.show()

    plt.hist(iris.T[3].astype(float))
    plt.xlabel('Largura petal em cm')
    plt.ylabel('Frequencia')
    plt.show()

def exercicio24a():
    adult = load_dataset('adult.data')
    for linha in adult:
        linha[1] = 'Private' if linha[1] == '?' else linha[1]
        linha[6] = 'Tech-Support' if linha[6] == '?' else linha[6]
        linha[13] = 'United-States' if linha[13] == '?' else linha[13]
    filename = 'adult-ex24a.data'
    save_dataset(adult, filename)
    print("Dados inputados salvos em ", filename)

def moda(dataset):
    rank = OrderedDict()
    for d in dataset:
        if d in rank:
            rank[d] += 1
        else:
            rank[d] = 1
    mais_comum = sorted(rank.values())[-1]
    indice_mais_comum = rank.values().index(mais_comum)
    return rank.keys()[indice_mais_comum]

def exercicio24b():
    adult = load_dataset('adult.data')
    for linha in adult:
        linha[1] =  moda(adult.T[1]) if linha[1] == '?' else linha[1]
        linha[6] = moda(adult.T[6]) if linha[6] == '?' else linha[6]
        linha[13] = moda(adult.T[13]) if linha[13] == '?' else linha[13]
    filename = 'adult-ex24b.data'
    save_dataset(adult, filename)
    print("Dados inputados salvos em ", filename)

def minmax(x, xi):
    return (float(xi) - min(x))/(float(max(x))-min(x))

def exercicio25a():
    cancer = load_dataset('breast-cancer-wisconsin.data')
    # inputa os valores faltantes:
    for linha in cancer:
        sem_faltantes = np.array([i for i in cancer.T[6] if i != '?']).astype(float)
        linha[6] =  np.median(sem_faltantes) if linha[6] == '?' else linha[6]

    #normaliza utilizando min-max
    for numlinha, linha in enumerate(cancer.astype(float)):
        for numcoluna, coluna in enumerate(linha):
            if numcoluna != 0: #ignora a coluna de ID
                cancer[numlinha][numcoluna] = minmax(cancer.T[numcoluna].astype(float), float(cancer[numlinha][numcoluna]))
    filename = 'cancer-ex25a.data'
    save_dataset(cancer, filename)
    print("Dados normalizados com min max salvos em ", filename)

def z_score(x, xi):
    xbarra = np.median(x)
    numerador = xi-xbarra
    return numerador/np.std(x)

def exercicio25b():
    cancer = load_dataset('breast-cancer-wisconsin.data')
    # inputa os valores faltantes:
    for linha in cancer:
        sem_faltantes = np.array([i for i in cancer.T[6] if i != '?']).astype(float)
        linha[6] =  np.median(sem_faltantes) if linha[6] == '?' else linha[6]

    #normaliza utilizando min-max
    for numlinha, linha in enumerate(cancer.astype(float)):
        for numcoluna, coluna in enumerate(linha):
            if numcoluna != 0: #ignora a coluna de ID
                cancer[numlinha][numcoluna] = z_score(cancer.T[numcoluna].astype(float), float(cancer[numlinha][numcoluna]))
    filename = 'cancer-ex25b.data'
    save_dataset(cancer, filename)
    print("Dados normalizados com escore-z salvos em ", filename)


# pesquisar distancia de quartis, gráfico de dispersão, box plot
if __name__ == '__main__':
    funcoes_disponiveis = {'exercicio23b': exercicio23b, 'exercicio23c': exercicio23c, 'exercicio23d': exercicio23d,
            'exercicio24a': exercicio24a, 'exercicio24b': exercicio24b, 'exercicio25a': exercicio25a, 'exercicio25b': exercicio25b}
    if len(sys.argv) != 2 or sys.argv[1] not in funcoes_disponiveis:
        print("Uso: python exercicios.py ({})".format('|'.join(funcoes_disponiveis.keys())))
        print("Exemplo: python exercicios.py exercicio23c")
        sys.exit(1)
    funcao = sys.argv[1]
    funcoes_disponiveis[funcao]()
