# encoding: utf-8
"""
Primeiro exercício de computação evolutiva.
"""

from random import randint, random

def individuo():
    return [randint(0,1) for x in xrange(36)]

def populacao(tamanho):
    return [individuo() for x in range(tamanho)]

def fitness(individuo, objetivo):
    i = individuo
    f = 9+i[1]*i[4]-i[22]*i[13]+i[23]*i[3]-i[20]*i[9]+i[35]*i[14]-i[10]*i[25]+i[15]*i[16]+i[2]*i[32]*+i[27]*i[18]+i[11]*i[33]-i[30]*i[31]-i[21]*i[24]+i[34]*i[26]-i[28]*i[6]+i[7]*i[12]-i[5]*i[8]+i[17]*i[19]-i[0]*i[29]+i[22]*i[3]+i[20]*i[14]+i[25]*i[15]+i[30]*i[11]+i[24]*i[18]+i[6]*i[7]+i[8]*i[17]+i[0]*i[32]
    return f

def fitness_medio_populacao(populacao, objetivo):
    soma = sum([fitness(individuo, objetivo) for individuo in populacao])
    return soma/len(populacao)

def evolucao(populacao, objetivo, retencao=0.2, selecao_aleatoria=0.05, mutacao=0.01):
    avaliacao = [(objetivo - fitness(individuo, objetivo), individuo) for individuo in populacao]
    avaliacao = [x[1] for x in sorted(avaliacao)]
    qtd_retencao = int(len(avaliacao)*retencao)
    pais = avaliacao[:qtd_retencao]

    # adiciona novos individuos
    for individuo in avaliacao[qtd_retencao:]:
        if selecao_aleatoria >= random():
            pais.append(individuo)

    #faz mutacao de alguns indivíduos
    for individuo in pais:
        if mutacao > random():
            posicao_da_mutacao = randint(0, len(individuo)-1)
            individuo[posicao_da_mutacao] = 1-individuo[posicao_da_mutacao]

    #faz o crossover dos pais para criar os filhos
    qtd_pais = len(pais)
    tamanho_desejado = len(populacao) - qtd_pais
    filhos = []
    while len(filhos) < tamanho_desejado:
        macho = randint(0, qtd_pais-1)
        femea = randint(0, qtd_pais-1)
        if macho != femea:
            macho = pais[macho]
            femea = pais[femea]
            metade = len(macho)/2
            filho = macho[:metade] + femea[metade:]
            filhos.append(filho)
    pais.extend(filhos)
    return pais

pop = populacao(80)
objetivo = 26
print "Fitness medio da populacao aleatoria: ", fitness_medio_populacao(pop, objetivo)
i = 0
while True:
    i += 1
    pop = evolucao(pop, objetivo, mutacao=0.2)
    #print "Fitness medio da populacao: ", fitness_medio_populacao(pop, objetivo)
    avaliacao = [(objetivo - fitness(individuo, objetivo), individuo) for individuo in pop]
    melhor_fitness = fitness(avaliacao[0][1], objetivo)
    print "Melhor individuo: ", melhor_fitness
    if melhor_fitness == objetivo:
        print "Encontrado melhor individuo depois de {} geracoes: ".format(i), avaliacao[0][1]
        break
