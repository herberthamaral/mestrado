# encoding: utf-8
from __future__ import print_function
import math

def pearson1(x, y):
    """Fórmula aproximada de Pearson. Disponível no livro Guide to data mining, página 45"""
    if len(x) != len(y):
        raise ValueError('x e y tem tamanhos diferentes')
    numerador = sum([x[i]*y[i] for i in range(len(x))]) - sum(x)*sum(y)/len(x)
    denominador = math.sqrt(sum([math.pow(xi, 2) for xi in x]) - pow(sum(x), 2)/len(x))
    denominador *= math.sqrt(sum([math.pow(yi, 2) for yi in y]) - pow(sum(y), 2)/len(y))
    return numerador/denominador

def media(x):
    return float(sum(x))/len(x)

def pearson2(x, y):
    """Fórmula de Pearson. Disponível no livro Guide to data mining, página 44"""
    if len(x) != len(y):
        raise ValueError('x e y tem tamanhos diferentes')
    xbarra, ybarra = media(x), media(y)
    numerador = sum([(x[i] - xbarra)*(y[i] - ybarra) for i in range(len(x))])
    denominador = math.sqrt(sum([math.pow(x[i] - xbarra, 2)]))
    denominador *= math.sqrt(sum([math.pow(y[i] - ybarra, 2)]))
    return numerador/denominador

def variancia(x):
    xbarra = media(x)
    var = sum([math.pow(xi - xbarra, 2) for xi in x])/len(x)
    return var

def desvio_padrao(x):
    return math.sqrt(variancia(x))

def z_score(x, xi):
    xbarra = media(x)
    numerador = xi-xbarra
    return numerador/desvio_padrao(x)

def minmax(x, xi):
    return (float(xi) - min(x))/(float(max(x))-min(x))


nota1 = [8.0, 8.0, 8.5, 7.6, 5.8, 4.0, 3.0, 3.0]
nota2 = [7.9, 7.9, 8.3, 7.5, 5.9, 4.1, 3.2, 3.2]
horas_estudo = [27, 27, 28, 29, 10, 15, 19, 19]
print("Similaridade de notas: "+str(pearson1(nota1, nota2)))
z_score_nota1 = [z_score(nota1, z) for z in nota1]
z_score_horas_estudo = [z_score(horas_estudo, z) for z in horas_estudo]
print("Correlação entre o z-score de notas e de horas de estudo: "+str(pearson1(z_score_nota1, z_score_horas_estudo)))

# atividade 2

altura = [57, 33, 10, 48, 40, '?', 20, 30, 12, 40, '?', 60]
largura = [308, 230, 300, 150, 400, 200, 200, 150, 101, 46, 85, 127] # o sétimo valor, faltante na base original, foi calculado
aspecto = [5.4, 7.0, 30.0, 3.1, 10.0, '?', 10.0, 5.0, 8.4, 1.2, '?', 2.1]

# substituição pela média
altura_sem_interrogacao = [a for a in altura if a != '?']
media_altura = media(altura_sem_interrogacao)
altura = [a if a != '?' else media_altura for a in altura]

largura_sem_interrogacao = [l for l in largura if l != '?']
media_largura = media(largura_sem_interrogacao)
largura = [l if l != '?' else media_largura for l in largura]

aspecto_sem_interrogacao = [a for a in aspecto if a != '?']
media_aspecto = media(aspecto_sem_interrogacao)
aspecto = [a if a != '?' else media_aspecto for a in aspecto]

print("Altura" + str(altura))
print("Largura" + str(largura))
print("Aspecto" + str(aspecto))

altura_normalizada = [minmax(altura, xi) for xi in altura]
largura_normalizada = [minmax(largura, xi) for xi in largura]
aspecto_normalizado = [minmax(aspecto, xi) for xi in aspecto]

print("Altura normalizada" + str(altura_normalizada))
print("Largura normalizada" + str(largura_normalizada))
print("Aspecto normalizado" + str(aspecto_normalizado))

print("Correlação entre altura e largura "  + str(pearson1(altura_normalizada, largura_normalizada)))
print("Correlação entre largura e aspecto " + str(pearson1(largura_normalizada, aspecto_normalizado)))
print("Correlação entre aspecto e altura "  + str(pearson1(aspecto_normalizado, altura_normalizada)))
