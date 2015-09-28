# encoding: utf-8
"""
Primeiro exercício de computação evolutiva.
"""
import sys
import numpy as np
import matplotlib.pyplot as plt
from random import randint, random, uniform, seed, shuffle

def individuo():
    return [randint(0,1) for x in range(36)]

def populacao(tamanho):
    return [individuo() for x in range(tamanho)]

def fitness(individuo):
    i = individuo
    f = 9+i[1]*i[4]-i[22]*i[13]+i[23]*i[3]-i[20]*i[9]+i[35]*i[14]-i[10]*i[25]+i[15]*i[16]+i[2]*i[32]\
            +i[27]*i[18]+i[11]*i[33]-i[30]*i[31]-i[21]*i[24]+i[34]*i[26]-i[28]*i[6]+i[7]*i[12]-i[5]\
            *i[8]+i[17]*i[19]-i[0]*i[29]+i[22]*i[3]+i[20]*i[14]+i[25]*i[15]+i[30]*i[11]+i[24]*i[18]\
            +i[6]*i[7]+i[8]*i[17]+i[0]*i[32]
    return f

media = lambda x: sum(x)/float(len(x))

def fitness_medio_populacao(populacao):
    return media([fitness(individuo) for individuo in populacao])

def ordena_melhores(populacao):
    melhores = [(fitness(individuo), individuo) for individuo in populacao]
    melhores = [x[1] for x in sorted(melhores)[::-1]]
    return melhores

def selecao_elitista(populacao, objetivo, retencao):
    melhores = ordena_melhores(populacao)
    qtd_retencao = int(len(melhores)*retencao)
    pais = melhores[:qtd_retencao]
    return pais

def selecao_roleta(populacao, objetivo, retencao):
    fitness_populacao = float(sum([fitness(i) for i in populacao]))
    fmp = fitness_medio_populacao(populacao)
    ordenado = ordena_melhores(populacao)
    def seleciona():
        p = 0
        for f in ordenado[::-1]:
            p += fitness(f)/(fitness_populacao*fmp)
            if random() <= p:
                break
        return f
    selecionados = []
    for x in range(int(len(populacao)*(1-retencao))):
        selecionado = seleciona()
        selecionados.append(selecionado)
    return selecionados

def selecao_torneio(populacao, objetivo, retencao):
    t = len(populacao)-1
    num_individuos = int(len(populacao)*retencao)
    selecionados = []
    for i in range(num_individuos/2):
        i1, i2 = populacao[randint(0,t)], populacao[randint(0,t)]
        i3, i4 = populacao[randint(0,t)], populacao[randint(0,t)]
        selecionados.append(i1 if fitness(i1) > fitness(i2) else i2)
        selecionados.append(i3 if fitness(i3) > fitness(i4) else i4)
    return selecionados

def mutacao_normal(individuos, taxa_mutacao):
    for individuo in individuos:
        if taxa_mutacao > random():
            posicao_da_mutacao = randint(0, len(individuo)-1)
            individuo[posicao_da_mutacao] = 1-individuo[posicao_da_mutacao]
    return individuos

def mutacao_uniforme(individuos, taxa_mutacao):
    for i, individuo in enumerate(individuos):
        for c, cromossomo in enumerate(individuo):
            if random() < taxa_mutacao:
                individuos[i][c] = 1-individuos[i][c]
    return individuos


def cruzamento_ponto_corte_aleatorio(pais, populacao, probabilidade):
    qtd_pais = len(pais)
    tamanho_desejado = len(populacao) - qtd_pais
    filhos = []
    while len(filhos) < tamanho_desejado:
        macho = randint(0, qtd_pais-1)
        femea = randint(0, qtd_pais-1)
        if macho != femea:
            macho = pais[macho]
            femea = pais[femea]
            pc = randint(0, 35)
            filho = macho[:pc] + femea[pc:]
            filhos.append(filho)
    return filhos

def cruzamento_uniforme(pais, populacao, probabilidade):
    qtd_pais = len(pais)
    tamanho_desejado = len(populacao) - qtd_pais
    filhos = []
    while len(filhos) < tamanho_desejado:
        macho = randint(0, qtd_pais-1)
        femea = randint(0, qtd_pais-1)
        macho = pais[macho]
        femea = pais[femea]
        if macho != femea:
            filho = []
            for i in range(36):
                if random() > 0.5:
                    filho.append(macho[i])
                else:
                    filho.append(femea[i])
            filhos.append(filho)
    return filhos

def evolucao(populacao, fitness, objetivo, retencao=0.2, taxa_mutacao=0.01, selecao=selecao_elitista,
        mutacao=mutacao_uniforme, cruzamento=cruzamento_ponto_corte_aleatorio, probabilidade_cruzamento=0.8):
    pais = selecao(populacao, objetivo, retencao)
    filhos = cruzamento(pais, populacao, probabilidade_cruzamento)
    filhos = mutacao(filhos, taxa_mutacao)
    pais.extend(filhos)
    return pais

def melhor_fitness(pop, objetivo=27):
    avaliacao = [(objetivo - fitness(i), i) for i in pop]
    melhor_fitness = fitness(avaliacao[0][1])
    return melhor_fitness

def menor_fitness(pop, objetivo=27):
    avaliacao = [(objetivo - fitness(i), i) for i in pop]
    melhor_fitness = fitness(avaliacao[0][1])
    return melhor_fitness


def teste_base(func_evolucao):
    dados_execucao = dict(numero_sucessos=0, maior_fitness=0, menor_fitness=0, fitness_medio=0, desvio_padrao=[])
    max_geracoes = 50
    execucoes = 100
    for i in range(execucoes):
        evolucao_melhor_fitness = []
        evolucao_fitness_medio = []
        perda_variedade_genetica = []
        p = populacao(30)
        geracoes = 0
        while geracoes<max_geracoes:
            incremento_taxa_mutacao = len(set(evolucao_melhor_fitness))*0.0
            p = func_evolucao(p, incremento_taxa_mutacao)
            geracoes += 1
            dados_execucao['desvio_padrao'].extend([fitness(j) for j in p])
            if dados_execucao['fitness_medio'] == 0:
                dados_execucao['fitness_medio'] = fitness_medio_populacao(p)
                dados_execucao['menor_fitness'] = melhor_fitness(p)
            else:
                dados_execucao['fitness_medio'] = media([dados_execucao['fitness_medio'], fitness_medio_populacao(p)])
                dados_execucao['menor_fitness'] = min([dados_execucao['menor_fitness'], menor_fitness(p)])
            evolucao_melhor_fitness.append(melhor_fitness(p))
            evolucao_fitness_medio.append(fitness_medio_populacao(p))
            perda_variedade_genetica.append(len(set([tuple(j) for j in p])))

        #print melhor_fitness(p)
        #plt.plot(range(len(evolucao_melhor_fitness)), evolucao_melhor_fitness, 'g')
        #plt.plot(range(len(evolucao_fitness_medio)), evolucao_fitness_medio, 'b')
        #plt.plot(range(len(perda_variedade_genetica)), perda_variedade_genetica, 'r')
        #plt.title(u'Evolução do melhor fitness e do fitness medio da população')
        ##import pdb;pdb.set_trace()
        #plt.show()

        dados_execucao['numero_sucessos'] += int(melhor_fitness(p) == 27)
        dados_execucao['maior_fitness'] = max(dados_execucao['maior_fitness'], melhor_fitness(p))
    dados_execucao['desvio_padrao'] = np.std(dados_execucao['desvio_padrao'])
    dados_execucao['execucoes'] = i+1
    return dados_execucao

def primeiro_teste():
    func_evolucao = lambda populacao, incremento_taxa_mutacao: evolucao(populacao, fitness, 27, selecao=selecao_roleta,
            retencao=0.8, taxa_mutacao=0.025+incremento_taxa_mutacao, cruzamento=cruzamento_ponto_corte_aleatorio)
    dados_execucao = teste_base(func_evolucao)
    print('\n'.join([chave+': '+str(dados_execucao[chave]) for chave in dados_execucao.keys()]))
    return dados_execucao

if __name__ == '__main__':
    funcoes_teste = dict(primeiro_teste=primeiro_teste)
    if len(sys.argv) != 2:
        print("Uso: caixapreta.py [teste]")
        print("Em que teste pode ser uma dentre: {}".format(', '.join(funcoes_teste.keys())))
        sys.exit(1)
    funcoes_teste[sys.argv[1]]()
