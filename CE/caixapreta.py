# encoding: utf-8
"""
Primeiro exercício de computação evolutiva.
"""

import sys
from random import randint, random, uniform, seed

seed()

def individuo():
    return [randint(0,1) for x in range(36)]

def populacao(tamanho):
    return [individuo() for x in range(tamanho)]

def fitness(individuo, objetivo):
    i = individuo
    f = 9+i[1]*i[4]-i[22]*i[13]+i[23]*i[3]-i[20]*i[9]+i[35]*i[14]-i[10]*i[25]+i[15]*i[16]+i[2]*i[32]+i[27]*i[18]+i[11]*i[33]-i[30]*i[31]-i[21]*i[24]+i[34]*i[26]-i[28]*i[6]+i[7]*i[12]-i[5]*i[8]+i[17]*i[19]-i[0]*i[29]+i[22]*i[3]+i[20]*i[14]+i[25]*i[15]+i[30]*i[11]+i[24]*i[18]+i[6]*i[7]+i[8]*i[17]+i[0]*i[32]
    return f

def fitness_medio_populacao(populacao, objetivo):
    soma = sum([fitness(individuo, objetivo) for individuo in populacao])
    return soma/len(populacao)

def ordena_melhores(populacao, objetivo):
    melhores = [(objetivo - fitness(individuo, objetivo), individuo) for individuo in populacao]
    melhores = [x[1] for x in sorted(melhores)]
    return melhores

def selecao_normal(populacao, objetivo, retencao):
    melhores = ordena_melhores(populacao, objetivo)
    qtd_retencao = int(len(melhores)*retencao)
    pais = melhores[:qtd_retencao]
    return pais

def selecao_roleta(populacao, objetivo, retencao):
    fitness_populacao = sum([fitness(i, objetivo) for i in populacao])
    ordenado = ordena_melhores(populacao, objetivo)
    def seleciona():
        p = uniform(0, fitness_populacao)
        for f in ordenado[::-1]:
            if p <= 0:
                break
            else:
                p -= fitness(f, objetivo)
        return f
    selecionados = []
    for x in range(int(len(populacao)*retencao)):
        selecionado = seleciona()
        ordenado.remove(selecionado)
        selecionados.append(selecionado)
    return selecionados

def selecao_torneio(populacao, objetivo, retencao):
    t = len(populacao)-1
    num_individuos = int(len(populacao)*retencao)
    selecionados = []
    for i in range(num_individuos/2):
        i1, i2 = populacao[randint(0,t)], populacao[randint(0,t)]
        i3, i4 = populacao[randint(0,t)], populacao[randint(0,t)]
        selecionados.append(i1 if fitness(i1, objetivo) > fitness(i2, objetivo) else i2)
        selecionados.append(i3 if fitness(i3, objetivo) > fitness(i4, objetivo) else i4)
    return selecionados

def mutacao_normal(individuos, taxa_mutacao):
    for individuo in individuos:
        if random() > taxa_mutacao:
            posicao_da_mutacao = randint(0, len(individuo)-1)
            individuo[posicao_da_mutacao] = 1-individuo[posicao_da_mutacao]
    return individuos

def mutacao_uniforme(individuos, taxa_mutacao):
    for i, individuo in enumerate(individuos):
        for c, cromossomo in enumerate(individuo):
            if random() > taxa_mutacao:
                individuos[i][c] = 1-individuos[i][c]
    return individuos


def cruzamento_normal(pais, populacao):
    qtd_pais = len(pais)
    tamanho_desejado = len(populacao) - qtd_pais
    filhos = []
    while len(filhos) < tamanho_desejado:
        macho = randint(0, qtd_pais-1)
        femea = randint(0, qtd_pais-1)
        if macho != femea:
            macho = pais[macho]
            femea = pais[femea]
            ponto_corte = randint(0, 35)
            filho = macho[:ponto_corte] + femea[ponto_corte:]
            filhos.append(filho)
    return filhos

def evolucao(populacao, objetivo, retencao=0.2, taxa_mutacao=0.01, selecao=selecao_normal, mutacao=mutacao_normal, cruzamento=cruzamento_normal):
    pais = selecao(populacao, objetivo, retencao)
    filhos = cruzamento(pais, populacao)
    filhos = mutacao(filhos, taxa_mutacao)
    pais.extend(filhos)
    return pais

if __name__ == '__main__':
    funcoes_selecao = {'selecao_roleta': selecao_roleta, 'selecao_torneio': selecao_torneio}
    if len(sys.argv) != 2:
        print("Uso: caixapreta.py funcao_selecao")
        print("As funções de seleção podem ser: {}".format(','.join(funcoes_selecao.keys())))
        sys.exit(1)
    selecao = funcoes_selecao[sys.argv[1]]
    objetivo = 27
    execucoes = []
    for v in range(30):
        pop = populacao(80)
        iteracoes = 0
        while True:
            iteracoes += 1
            pop = evolucao(pop, objetivo, taxa_mutacao=0.025, selecao=selecao)
            #print "Fitness medio da populacao: ", fitness_medio_populacao(pop, objetivo)
            avaliacao = [(objetivo - fitness(i, objetivo), i) for i in pop]
            melhor_fitness = fitness(avaliacao[0][1], objetivo)
            #print "Melhor individuo: ", melhor_fitness
            if melhor_fitness == objetivo:
                print "Encontrado melhor individuo depois de {} geracoes: ".format(iteracoes), avaliacao[0][1]
                execucoes.append(iteracoes)
                break
    print("Quantidade média de gerações: {}".format(sum(execucoes)/float(len(execucoes))))
