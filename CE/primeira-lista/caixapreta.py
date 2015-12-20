# encoding: utf-8
"""
Primeiro exercício de computação evolutiva.
"""
import sys
import math
import numpy as np
from scipy.stats import ranksums
from random import randint, random, uniform, seed, shuffle

seed(123456)

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
variancia = lambda x: sum([math.pow(xi - media(x), 2) for xi in x])/len(x)
desvio_padrao = lambda x: math.sqrt(variancia(x))
mediana = lambda x: sorted(x)[(len(x)/2)] if len(x)%2==1 else media(sorted(x)[len(x)/2-1:len(x)/2+1])
pc = np.percentile

def fitness_medio_populacao(populacao):
    return media([fitness(individuo) for individuo in populacao])

def ordena_melhores(populacao):
    melhores = [(fitness(individuo), individuo) for individuo in populacao]
    melhores = [x[1] for x in sorted(melhores)[::-1]]
    return melhores

def selecao_roleta(populacao):
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
    selecionados = [seleciona(), seleciona()]
    return selecionados

def selecao_torneio(populacao):
    t = len(populacao)-1
    selecionados = []
    i1, i2 = populacao[randint(0,t)], populacao[randint(0,t)]
    i3, i4 = populacao[randint(0,t)], populacao[randint(0,t)]
    selecionados.append(i1 if fitness(i1) > fitness(i2) else i2)
    selecionados.append(i3 if fitness(i3) > fitness(i4) else i4)
    return selecionados

def mutacao_escolha_aleatoria_do_bit(individuos, taxa_mutacao):
    for individuo in individuos:
        if taxa_mutacao > random():
            posicao_da_mutacao = randint(0, len(individuo)-1)
            individuo[posicao_da_mutacao] = 1-individuo[posicao_da_mutacao]
    return individuos

def mutacao_bit_a_bit(individuos, taxa_mutacao):
    for i, individuo in enumerate(individuos):
        for c, cromossomo in enumerate(individuo):
            if random() < taxa_mutacao:
                individuos[i][c] = 1-individuos[i][c]
    return individuos

def cruzamento_ponto_corte_aleatorio(pais):
    filhos = []
    for ps in pais:
        pc = randint(0, len(pais[0])-1)
        filho1 = ps[0][:pc] + ps[1][pc:]
        filho2 = ps[1][:pc] + ps[0][pc:]
        filhos.extend([filho1, filho2])
    return filhos

def cruzamento_uniforme(pais):
    pc = len(pais[0][0])/2
    filhos = []
    for ps in pais:
        filho1 = ps[0][:pc] + ps[1][pc:]
        filho2 = ps[1][:pc] + ps[0][pc:]
        filhos.extend([filho1, filho2])
    return filhos

def melhor_fitness(pop):
    return min([fitness(p) for p in pop])

def pior_fitness(pop):
    return max([fitness(p) for p in pop])

def media_fitness(pop):
    return media([fitness(p) for p in pop])

def selecao(pop, funcao, prob_mutacao, N):
    return [funcao(pop) for i in range(N) if prob_mutacao > random()]

def substituicao_elitista(pop, filhos, N):
    pop.extend(filhos)
    proxima_geracao = sorted([(fitness(f),f) for f in pop], reverse=True)[:N]
    pop = [p[1] for p in proxima_geracao]
    return pop 

def substituicao_nao_elitista(pop, filhos, N):
    pop.extend(filhos)
    shuffle(pop)
    return pop[:N]

def evolucao(N = 30,prob_cruzamento = 0.8,
                   prob_mutacao = 0.025,
                   num_geracoes = 50,
                   funcao_selecao=selecao_roleta,
                   cruzamento=cruzamento_uniforme,
                   mutacao=mutacao_escolha_aleatoria_do_bit,
                   substituicao=substituicao_nao_elitista, **kwargs):
    mf = []
    pop = populacao(N)
    for g in range(num_geracoes):
        pais = selecao(pop, funcao_selecao, prob_cruzamento, N)
        filhos = cruzamento(pais) if pais else []
        filhos = mutacao(filhos, prob_mutacao) if filhos else []
        pop = substituicao(pop, filhos, N) if filhos else pop
        fpop = map(fitness, pop)
        b, w, a, s = max(fpop), min(fpop), media(fpop), desvio_padrao(fpop)
        mf.append(b)
        #print '[{}] Melhor/Pior/Media/Std: {}/{}/{}/{}'.format(str(g).rjust(2, '0'), b, w, a, s)
    b, w, a, s = max(mf), min(mf), media(mf), desvio_padrao(mf)
    #print 'Fim da execução. Melhor/Pior/Media/Std: {}/{}/{}/{}'.format(b, w, a, s)
    return b,w,a,s

def stats_tests(a1, a2, a1label, a2label):
    p = ranksums(a1, a2)[1]
    if  p < 0.05:
        ma1 = mediana(a1)
        ma2 = mediana(a2)
        if ma1 > ma2:
            b, w, a, s = max(a1), min(a1), media(a1), desvio_padrao(a1)
            q1, q2, q3 = pc(a1, 25), pc(a1, 50), pc(a1, 75)
            sucessos = len([f for f in a1 if f == 27])
        else:
            b, w, a, s = max(a2), min(a2), media(a2), desvio_padrao(a2)
            q1, q2, q3 = pc(a2, 25), pc(a2, 50), pc(a2, 75)
            sucessos = len([f for f in a1 if f == 27])
        print '{} ({}) > {} ({}) - p={}'.format(a1label, ma1, a2label, ma2, p) if ma1 > ma2 else '{} ({}) > {} ({}) - p={}'.format(a2label, ma2, a1label, ma1, p)
        print 'Maior/Menor/Media/Desvio/Sucessos: {}/{}/{}/{}/{}'.format(b,w,a,s,sucessos)
        print 'Q1/Q2/Q3/ {}/{}/{}'.format(q1, q2, q3)
    else:
        print u'Diferença não significativa estatisticamente (p={})'.format(p)

def primeiro_teste(N = 30,prob_cruzamento = 0.8,
                   prob_mutacao = 0.025,
                   num_geracoes = 50,
                   funcao_selecao=selecao_roleta,
                   cruzamento=cruzamento_ponto_corte_aleatorio,
                   mutacao=mutacao_escolha_aleatoria_do_bit,
                   substituicao=substituicao_nao_elitista):
    melhores_aleatorio = []
    melhores_uniforme = []
    for e in range(60):
        cruzamento = cruzamento_ponto_corte_aleatorio
        melhores_aleatorio.append(evolucao(**locals())[0])
        cruzamento = cruzamento_uniforme 
        melhores_uniforme.append(evolucao(**locals())[0])
    stats_tests(melhores_uniforme, melhores_aleatorio, 'Uniforme', 'Aleatorio')

def segundo_teste(N = 30,prob_cruzamento = 0.8,
                  prob_mutacao = 0.025,
                  num_geracoes = 50,
                  funcao_selecao=selecao_roleta,
                  cruzamento=cruzamento_uniforme,
                  mutacao=mutacao_bit_a_bit,
                  substituicao=substituicao_nao_elitista):
    melhores_roleta = []
    melhores_torneio = []
    for e in range(60):
        funcao_selecao = selecao_roleta
        melhores_roleta.append(evolucao(**locals())[0])
        funcao_selecao = selecao_torneio
        melhores_torneio.append(evolucao(**locals())[0])
    stats_tests(melhores_roleta, melhores_torneio, 'Roleta', 'Torneio')

def terceiro_teste(N = 30,prob_cruzamento = 0.8,
                   prob_mutacao = 0.025,
                   num_geracoes = 50,
                   funcao_selecao=selecao_roleta,
                   cruzamento=cruzamento_uniforme,
                   mutacao=mutacao_bit_a_bit,
                   substituicao=substituicao_nao_elitista):
    melhores_bab = []
    melhores_aleatorio = []
    for e in range(60):
        mutacao = mutacao_bit_a_bit
        melhores_bab.append(evolucao(**locals())[0])
        mutacao = mutacao_escolha_aleatoria_do_bit
        melhores_aleatorio.append(evolucao(**locals())[0])
    stats_tests(melhores_bab, melhores_aleatorio, 'Bit-a-bit', 'Aleatório')

def quarto_teste(N = 30,prob_cruzamento = 0.8,
                 prob_mutacao = 0.025,
                 num_geracoes = 50,
                 funcao_selecao=selecao_roleta,
                 cruzamento=cruzamento_uniforme,
                 mutacao=mutacao_bit_a_bit,
                 substituicao=substituicao_nao_elitista):
    melhores02, melhores05, melhores08 = [], [], []
    for e in range(60):
        prob_cruzamento = 0.2
        melhores02.append(evolucao(**locals())[0])
        prob_cruzamento = 0.5
        melhores05.append(evolucao(**locals())[0])
        prob_cruzamento = 0.8
        melhores08.append(evolucao(**locals())[0])
    stats_tests(melhores02, melhores05, '20%', '50%')
    stats_tests(melhores02, melhores08, '20%', '80%')
    stats_tests(melhores05, melhores08, '50%', '80%')

def quinto_teste(N = 30,prob_cruzamento = 0.8,
                 prob_mutacao = 0.025,
                 num_geracoes = 50,
                 funcao_selecao=selecao_roleta,
                 cruzamento=cruzamento_uniforme,
                 mutacao=mutacao_bit_a_bit,
                 substituicao=substituicao_nao_elitista):
    melhores1, melhores2meio, melhores5, melhores10, melhores25, melhores75 = [], [], [], [], [], []
    for e in range(60):
        prob_mutacao = 0.001
        melhores1.append(evolucao(**locals())[0])
        prob_mutacao = 0.025
        melhores2meio.append(evolucao(**locals())[0])
        prob_mutacao = 0.05
        melhores5.append(evolucao(**locals())[0])
        prob_mutacao = 0.1
        melhores10.append(evolucao(**locals())[0])
        prob_mutacao = 0.25
        melhores25.append(evolucao(**locals())[0])
        prob_mutacao = 0.75
        melhores75.append(evolucao(**locals())[0])
    stats_tests(melhores2meio, melhores5, '2.5%', '5%')
    stats_tests(melhores2meio, melhores10, '2.5%', '10%')
    stats_tests(melhores2meio, melhores25, '2.5%', '25%')
    stats_tests(melhores2meio, melhores75, '2.5%', '75%')
    stats_tests(melhores5, melhores10, '5%', '10%')
    stats_tests(melhores5, melhores25, '5%', '25%')
    stats_tests(melhores5, melhores75, '5%', '75%')
    stats_tests(melhores10, melhores25, '10%', '25%')
    stats_tests(melhores10, melhores75, '10%', '75%')
    stats_tests(melhores25, melhores75, '25%', '75%')

def sexto_teste(N = 30,prob_cruzamento = 0.8,
                 prob_mutacao = 0.025,
                 num_geracoes = 50,
                 funcao_selecao=selecao_roleta,
                 cruzamento=cruzamento_uniforme,
                 mutacao=mutacao_bit_a_bit,
                 substituicao=substituicao_elitista):
    melhores_elitismo, melhores_random = [], []
    for e in range(60):
        substituicao = substituicao_elitista
        melhores_elitismo.append(evolucao(**locals())[0])
        substituicao = substituicao_nao_elitista
        melhores_random.append(evolucao(**locals())[0])
    stats_tests(melhores_elitismo, melhores_random, 'Elitismo', 'Aleatorio')

def sexto_teste_torneio(N = 30,prob_cruzamento = 0.8,
                 prob_mutacao = 0.025,
                 num_geracoes = 50,
                 funcao_selecao=selecao_torneio,
                 cruzamento=cruzamento_uniforme,
                 mutacao=mutacao_bit_a_bit,
                 substituicao=substituicao_elitista): 
    melhores_elitismo, melhores_random = [], []
    for e in range(60):
        substituicao = substituicao_elitista
        melhores_elitismo.append(evolucao(**locals())[0])
        substituicao = substituicao_nao_elitista
        melhores_random.append(evolucao(**locals())[0])
    stats_tests(melhores_elitismo, melhores_random, 'Elitismo (torneio)', 'Aleatorio (torneio)')

def teste_num_geracoes(N = 30,prob_cruzamento = 0.8,
                       prob_mutacao = 0.025,
                       num_geracoes = 50,
                       funcao_selecao=selecao_roleta,
                       cruzamento=cruzamento_uniforme,
                       mutacao=mutacao_bit_a_bit,
                       substituicao=substituicao_elitista):
    melhores_20, melhores_25, melhores_30, melhores_50= [], [], [], []
    for e in range(50):
        num_geracoes = 20
        melhores_20.append(evolucao(**locals())[0])
        num_geracoes = 25
        melhores_25.append(evolucao(**locals())[0])
        num_geracoes = 30
        melhores_30.append(evolucao(**locals())[0])
        num_geracoes = 50
        melhores_50.append(evolucao(**locals())[0])
    stats_tests(melhores_20, melhores_25, '20', '25')
    stats_tests(melhores_20, melhores_30, '20', '30')
    stats_tests(melhores_20, melhores_50, '20', '50')
    stats_tests(melhores_25, melhores_30, '25', '30')
    stats_tests(melhores_25, melhores_50, '25', '50')
    stats_tests(melhores_30, melhores_50, '30', '50')

def teste_num_individuos(N=20,prob_cruzamento = 0.8,
                       prob_mutacao = 0.025,
                       num_geracoes = 25,
                       funcao_selecao=selecao_roleta,
                       cruzamento=cruzamento_uniforme,
                       mutacao=mutacao_bit_a_bit,
                       substituicao=substituicao_elitista):
    melhores_10, melhores_20, melhores_25, melhores_30, melhores_50= [], [], [], [], []
    for e in range(60):
        N = 10
        melhores_10.append(evolucao(**locals())[0])
        N = 20
        melhores_20.append(evolucao(**locals())[0])
        N = 25
        melhores_25.append(evolucao(**locals())[0])
        N = 30
        melhores_30.append(evolucao(**locals())[0])
        N = 50
        melhores_50.append(evolucao(**locals())[0])
    stats_tests(melhores_10, melhores_20, '10', '20')
    stats_tests(melhores_10, melhores_25, '10', '25')
    stats_tests(melhores_10, melhores_30, '10', '30')
    stats_tests(melhores_10, melhores_50, '10', '50')
    stats_tests(melhores_20, melhores_25, '20', '25')
    stats_tests(melhores_20, melhores_30, '20', '30')
    stats_tests(melhores_20, melhores_50, '20', '50')
    stats_tests(melhores_25, melhores_30, '25', '30')
    stats_tests(melhores_25, melhores_50, '25', '50')
    stats_tests(melhores_30, melhores_50, '30', '50')


if __name__ == '__main__':
    funcoes_teste = dict(primeiro_teste=primeiro_teste,
                         segundo_teste=segundo_teste,
                         terceiro_teste=terceiro_teste,
                         quarto_teste=quarto_teste,
                         quinto_teste=quinto_teste,
                         sexto_teste=sexto_teste,
                         teste_num_geracoes=teste_num_geracoes,
                         teste_num_individuos=teste_num_individuos,
                         sexto_teste_torneio=sexto_teste_torneio)
    if len(sys.argv) != 2:
        print("Uso: caixapreta.py [teste]")
        print("Em que teste pode ser uma dentre: {}".format(', '.join(funcoes_teste.keys())))
        sys.exit(1)
    funcoes_teste[sys.argv[1]]()
