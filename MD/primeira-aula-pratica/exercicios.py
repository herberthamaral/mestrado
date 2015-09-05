#!/usr/bin/env python
# encoding: utf-8
from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr, spearmanr
from chauvenet import chauvenet

#carrega dados do iris
iris = open('iris.data', 'r').read().split('\n')
iris = [[float(i) for i in linha.split(',')[:-1]] for linha in iris if linha]
iris = np.array(iris)

correlacoes = [(0,1), (0,2), (0,3), (1,2), (1,3), (2,3)]
correlacoes_labels = ['altura sepal', 'largura sepal', 'altura petal', 'largura petal']

# Gráfico com os dados ordenados
for i,c in enumerate(correlacoes_labels):
    plt.plot(range(len(iris.T[i])), sorted(iris.T[i]), 'ro')
    plt.title('{}'.format(correlacoes_labels[i]))
    plt.show()

for c in correlacoes:
    p = pearsonr(iris.T[c[0]], iris.T[c[1]])[0]
    correlacao_grau = 'baixa' if abs(p) < 0.6 else 'alta'
    correlacao_tipo = 'inversamente proporcional' if p < 0 else 'diretamente proporcional'
    print("Correlação linear entre {0} e {1}: {2}, {3} e {4}".format(correlacoes_labels[c[0]], correlacoes_labels[c[1]], p, correlacao_grau, correlacao_tipo))

# Analisando os gráficos anteriores, nota-se que as funções não são exatamente lineares.
# por este motivo estou usando a correlação de spearman também
print("\n\n\n\n\n--------------------------------%<-------------------------------\n\n\n\n\n")
for c in correlacoes:
    p = spearmanr(iris.T[c[0]], iris.T[c[1]])[0]
    correlacao_grau = 'baixa' if abs(p) < 0.6 else 'alta'
    correlacao_tipo = 'inversamente proporcional' if p < 0 else 'diretamente proporcional'
    print("Correlação monotônica entre {0} e {1}: {2}, {3} e {4}".format(correlacoes_labels[c[0]], correlacoes_labels[c[1]], p, correlacao_grau, correlacao_tipo))

for i, c in enumerate(correlacoes_labels):
    qtd = len([x for x in chauvenet(iris.T[i]) if not x])
    if qtd > 0:
        pos = [l for l in chauvenet(iris.T[i])].index(False)
        print("--Outlier na posição ", pos)
    print("Num outliers (utilizando o critério de Chauvenet) em {}: {}".format(c, qtd))

plt.hist(iris.T[0])
plt.xlabel('Altura sepal em cm')
plt.ylabel('Frequencia')
plt.show()

plt.hist(iris.T[1])
plt.xlabel('Largura sepal em cm')
plt.ylabel('Frequencia')
plt.show()

plt.hist(iris.T[2])
plt.xlabel('Altura petal em cm')
plt.ylabel('Frequencia')
plt.show()

plt.hist(iris.T[3])
plt.xlabel('Largura petal em cm')
plt.ylabel('Frequencia')
plt.show()

# distancia de quartis, gráfico de dispersão, box plot
