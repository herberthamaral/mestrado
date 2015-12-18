#encoding: utf-8
import sys
import random
import json
import time
import datetime
from multiprocessing import Pool, cpu_count
from pontes import executa, cria_estagios, cria_pontes
from ordem_servico import gera_individuo

def calcula_fitness(individuo):
    return executa(cria_pontes(), cria_estagios(), individuo[0])

POOL = None
DEBUG = '--debug' in sys.argv

# primeira dimensão da população: lista de indivíduos (individuos[0..100])
# segunda dimensão da população: (individuo, Fitness) (individuos[0..100][0..1900], individuos[0..100][1])
# terceira dimensão da população (dentro do indivíduo): transicao (individuos[0..100][0..1900][0])

def inicializa_populacao(n):
    individuos = [[gera_individuo(), None] for i in range(n)]
    return calcula_finess_faltantes(individuos)

def calcula_finess_faltantes(individuos):
    global POOL
    global DEBUG
    if not POOL and not DEBUG:
        POOL = Pool(cpu_count()/2)
    individuos_com_fitness = [i for i in individuos if i[1]]
    individuos_sem_fitness = [i for i in individuos if not i[1]]
    fitnesses = []
    if not DEBUG:
        fitnesses = POOL.map(calcula_fitness, individuos_sem_fitness)
    else:
        for i in individuos_sem_fitness:
            fitnesses.append(calcula_fitness(i))

    novos_individuos_com_fitness = []
    for i, fitness in enumerate(fitnesses):
        individuos_sem_fitness[i][1] = fitness
        novos_individuos_com_fitness.append(individuos_sem_fitness[i])
    return individuos_com_fitness+novos_individuos_com_fitness


def cruzamento(individuos, num_filhos):
    pai1 = pai2 = None
    chance_pai1 = 0.5
    for n in range(num_filhos/2):
        while pai1 == pai2:
            pai1 = random.choice(individuos[:10])
            pai2 = random.choice(individuos[:10])
        filho1 = []
        filho2 = []
        for pos in range(len(pai1[0])-1):
            if chance_pai1 > random.random():
                filho1.append(pai1[0][pos])
                filho2.append(pai2[0][pos])
            else:
                filho1.append(pai2[0][pos])
                filho2.append(pai1[0][pos])
        individuos.append([filho1, None])
        individuos.append([filho2, None])
    return individuos

def mutacao(individuos, chance_mutacao):
    i = 0
    qtd_cromossomos = len(individuos[0][0])
    posicao = random.randint(0, qtd_cromossomos-1)
    mutados = 0
    qtd_mudancas = int(qtd_cromossomos*chance_mutacao)
    i = 0
    while i < len(individuos):
        if chance_mutacao > random.random():
            mutados += 1
            posicao_cromossomos_mudados = []
            for j in range(qtd_mudancas):
                while posicao in posicao_cromossomos_mudados or len(individuos[i][0]) < posicao or not individuos[i][0][posicao].get('possiveis'):
                    posicao = random.randint(0, qtd_cromossomos-1)
                individuos[i][0][posicao]['ponte'] = random.choice(individuos[i][0][posicao]['possiveis'])
                individuos[i][1] = None
                posicao_cromossomos_mudados.append(posicao)
        i += 1
    return individuos

now = lambda: datetime.datetime.now().time().strftime('%Hh%Mm%Ss')

def salva_execucao(geracao, inicio_exec, inicio, individuos, evolucao_execucao):
    fim = datetime.datetime.now()
    g = str(geracao).rjust(5, '0')
    print '[G{}][{}] Pior fitness {}'.format(g, now(), individuos[-1][1])
    print '[G{}][{}] Melhor fitness {}'.format(g, now(), individuos[0][1])
    evolucao_execucao.append(((fim-inicio).total_seconds(), individuos[0]))
    with open('execucao-{hora}.json'.format(hora=inicio_exec), 'w') as arquivo:
        arquivo.write(json.dumps(evolucao_execucao))
    return evolucao_execucao

def selecao(individuos, N):
    selecionados = []
    return individuos[:N]

def deduplica(individuos):
    unicos = []
    return [unicos.append(individuo) for individuo in individuos if individuo not in unicos and len(individuo) == 1922]

def ag():
    N = 100
    inicio_exec = now()
    individuos = inicializa_populacao(N)
    evolucao_execucao = []
    melhor = sorted(individuos, key=lambda k: k[1])[0]
    for geracao in range(200):
        inicio = datetime.datetime.now()
        individuos = cruzamento(individuos, 10)
        individuos = mutacao(individuos, 0.02)
        individuos = deduplica(individuos)
        individuos = individuos + inicializa_populacao(N-len(individuos))
        individuos = calcula_finess_faltantes(individuos)
        individuos = sorted(individuos, key=lambda k: k[1])
        individuos = selecao(individuos, N)
        melhor = individuos[0] if individuos[0][1] < melhor else melhor
        evolucao_execucao = salva_execucao(geracao, inicio_exec, inicio, individuos, evolucao_execucao)
    print 'Melhor fitness: {}'.format(melhor[1])

if __name__ == '__main__':
    for ex in range(30):
        ag()
