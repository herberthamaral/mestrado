# encoding: utf-8
"""
Primeiro exercício de computação evolutiva.
"""
import sys
import math
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
variancia = lambda x: sum([math.pow(xi - media(x), 2) for xi in x])/len(x)
desvio_padrao = lambda x: math.sqrt(variancia(x))

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

def primeiro_teste(N = 30,prob_cruzamento = 0.8,
                   prob_mutacao = 0.025,
                   num_geracoes = 50,
                   funcao_selecao=selecao_roleta,
                   cruzamento=cruzamento_ponto_corte_aleatorio,
                   mutacao=mutacao_escolha_aleatoria_do_bit,
                   substituicao=substituicao_nao_elitista):
    melhores_aleatorio = []
    melhores_uniforme = []
    for e in range(50):
        cruzamento = cruzamento_ponto_corte_aleatorio
        melhores_aleatorio.append(evolucao(**locals())[0])
        cruzamento = cruzamento_uniforme 
        melhores_uniforme.append(evolucao(**locals())[0])
    mu = media(melhores_uniforme)
    ma = media(melhores_aleatorio)
    print 'Uniforme ({}) > Aleatorio ({})'.format(mu, ma) if mu > ma else 'Aleatorio ({}) > Uniforme ({})'.format(ma, mu)

def segundo_teste(N = 30,prob_cruzamento = 0.8,
                  prob_mutacao = 0.025,
                  num_geracoes = 50,
                  funcao_selecao=selecao_roleta,
                  cruzamento=cruzamento_uniforme,
                  mutacao=mutacao_bit_a_bit,
                  substituicao=substituicao_nao_elitista):
    melhores_roleta = []
    melhores_torneio = []
    for e in range(50):
        funcao_selecao = selecao_roleta
        melhores_roleta.append(evolucao(**locals())[0])
        funcao_selecao = selecao_torneio
        melhores_torneio.append(evolucao(**locals())[0])
    mr = media(melhores_roleta)
    mt = media(melhores_torneio)
    print 'Torneio ({}) > Roleta ({})'.format(mt, mr) if mt > mr else 'Roleta ({}) > Torneio ({})'.format(mr, mt)

def terceiro_teste(N = 30,prob_cruzamento = 0.8,
                   prob_mutacao = 0.025,
                   num_geracoes = 50,
                   funcao_selecao=selecao_roleta,
                   cruzamento=cruzamento_uniforme,
                   mutacao=mutacao_bit_a_bit,
                   substituicao=substituicao_nao_elitista):
    melhores_bab = []
    melhores_aleatorio = []
    for e in range(50):
        mutacao = mutacao_bit_a_bit
        melhores_bab.append(evolucao(**locals())[0])
        mutacao = mutacao_escolha_aleatoria_do_bit
        melhores_aleatorio.append(evolucao(**locals())[0])
    mb = media(melhores_bab)
    ma = media(melhores_aleatorio)
    print 'Bit-a-bit ({}) > Aleatorio ({})'.format(mb, ma) if mb > ma else 'Aleatorio ({}) > Bit-a-bit ({})'.format(ma, mb)
    return evolucao(**locals())

def quarto_teste(N = 30,prob_cruzamento = 0.8,
                 prob_mutacao = 0.025,
                 num_geracoes = 50,
                 funcao_selecao=selecao_roleta,
                 cruzamento=cruzamento_uniforme,
                 mutacao=mutacao_bit_a_bit,
                 substituicao=substituicao_nao_elitista):
    melhores02, melhores05, melhores08 = [], [], []
    for e in range(50):
        prob_cruzamento = 0.2
        melhores02.append(evolucao(**locals())[0])
        prob_cruzamento = 0.5
        melhores05.append(evolucao(**locals())[0])
        prob_cruzamento = 0.8
        melhores08.append(evolucao(**locals())[0])
    m2 = media(melhores02)
    m5 = media(melhores05)
    m8 = media(melhores08)
    print '0.2, 0.5, 0.8: {}, {}, {}'.format(m2,m5,m8)
    return evolucao(**locals())

def quinto_teste(N = 30,prob_cruzamento = 0.8,
                 prob_mutacao = 0.025,
                 num_geracoes = 50,
                 funcao_selecao=selecao_roleta,
                 cruzamento=cruzamento_uniforme,
                 mutacao=mutacao_bit_a_bit,
                 substituicao=substituicao_nao_elitista):
    melhores1, melhores2meio, melhores5, melhores10, melhores25, melhores75 = [], [], [], [], [], []
    for e in range(50):
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
    medias = (media(melhores1), media(melhores2meio), media(melhores5), media(melhores10), media(melhores25), media(melhores75))
    print '0.001, 0.025, 0.05, 0.1, 0.25, 0.75: {}, {}, {}, {}, {}, {}'.format(*medias)

def sexto_teste(N = 30,prob_cruzamento = 0.8,
                 prob_mutacao = 0.025,
                 num_geracoes = 50,
                 funcao_selecao=selecao_roleta,
                 cruzamento=cruzamento_uniforme,
                 mutacao=mutacao_bit_a_bit,
                 substituicao=substituicao_elitista):
    melhores_elitismo, melhores_random = [], []
    for e in range(50):
        substituicao = substituicao_elitista
        melhores_elitismo.append(evolucao(**locals())[0])
        substituicao = substituicao_nao_elitista
        melhores_random.append(evolucao(**locals())[0])
    print 'Elitismo: {}, Sem elitismo: {}'.format(media(melhores_elitismo), media(melhores_random))
    return evolucao(**locals())

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
    print '20: {}, 25: {}, 30: {}, 50: {}'.format(media(melhores_20), media(melhores_25), media(melhores_30), media(melhores_50))
    return evolucao(**locals())

def teste_num_individuos(N = 30,prob_cruzamento = 0.8,
                       prob_mutacao = 0.025,
                       num_geracoes = 30,
                       funcao_selecao=selecao_roleta,
                       cruzamento=cruzamento_uniforme,
                       mutacao=mutacao_bit_a_bit,
                       substituicao=substituicao_elitista):
    melhores_10, melhores_20, melhores_25, melhores_30, melhores_50= [], [], [], [], []
    for e in range(50):
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
    print '10: {}, 20: {}, 25: {}, 30: {}, 50: {}'.format(media(melhores_10),media(melhores_20), media(melhores_25), media(melhores_30), media(melhores_50))
    return evolucao(**locals())


if __name__ == '__main__':
    funcoes_teste = dict(primeiro_teste=primeiro_teste,
                         segundo_teste=segundo_teste,
                         terceiro_teste=terceiro_teste,
                         quarto_teste=quarto_teste,
                         quinto_teste=quinto_teste,
                         sexto_teste=sexto_teste,
                         teste_num_geracoes=teste_num_geracoes,
                         teste_num_individuos=teste_num_individuos)
    if len(sys.argv) != 2:
        print("Uso: caixapreta.py [teste]")
        print("Em que teste pode ser uma dentre: {}".format(', '.join(funcoes_teste.keys())))
        sys.exit(1)
    funcoes_teste[sys.argv[1]]()
