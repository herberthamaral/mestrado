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
    for n in range(num_filhos):
        while pai1 == pai2:
            pai1 = random.choice(individuos)
            pai2 = random.choice(individuos)
        filho = []
        for pos in range(len(pai1[0])-1):
            if chance_pai1 > random.random():
                filho.append(pai1[0][pos])
            else:
                filho.append(pai2[0][pos])
        individuos.append([filho, None])
    return individuos

def mutacao(individuos, chance_mutacao):
    i = 0
    qtd_cromossomos = len(individuos[0][0])
    posicao = random.randint(0, qtd_cromossomos-1)
    mutados = 0
    qtd_mudancas = int(qtd_cromossomos*chance_mutacao)
    while i < len(individuos):
        if chance_mutacao > random.random():
            mutados += 1
            posicao_cromossomos_mudados = []
            for j in range(qtd_mudancas):
                try:
                    if len(individuos[i][0]) < posicao:
                        import pdb;pdb.set_trace()
                    while posicao in posicao_cromossomos_mudados or len(individuos[i][0]) < posicao or not individuos[i][0][posicao].get('possiveis'):
                        posicao = random.randint(0, qtd_cromossomos-1)
                        if len(individuos[i][0]) < posicao:
                            import pdb;pdb.set_trace()
                    individuos[i][0][posicao]['ponte'] = random.choice(individuos[i][0][posicao]['possiveis'])
                    individuos[i][1] = None
                    posicao_cromossomos_mudados.append(posicao)
                except IndexError:
                    import pdb;pdb.set_trace()
        i += 1
    return individuos

now = lambda: datetime.datetime.now().time().strftime('%Hh%Mm') 

def salva_execucao(geracao, inicio_exec, inicio, individuos, evolucao_execucao):
    fim = datetime.datetime.now()
    print '[G{}][{}] Pior fitness {}'.format(geracao, now(), individuos[-1][1])
    print '[G{}][{}] Melhor fitness {}'.format(geracao, now(), individuos[0][1])
    evolucao_execucao.append(((fim-inicio).total_seconds(), individuos[0]))
    with open('execucao-{hora}.json'.format(hora=inicio_exec), 'w') as arquivo:
        arquivo.write(json.dumps(evolucao_execucao))
    return evolucao_execucao

def selecao(individuos, N):
    return individuos[:N]


def ag():
    N = 60
    inicio_exec = now()
    individuos = inicializa_populacao(N)
    evolucao_execucao = []
    for geracao in range(60):
        inicio = datetime.datetime.now()
        individuos = cruzamento(individuos, 10)
        individuos = mutacao(individuos, 0.02)
        individuos = calcula_finess_faltantes(individuos)
        individuos = sorted(individuos, key=lambda k: k[1])
        individuos = selecao(individuos, N)
        evolucao_execucao = salva_execucao(geracao, inicio_exec, inicio, individuos, evolucao_execucao)

if __name__ == '__main__':
    ag()
