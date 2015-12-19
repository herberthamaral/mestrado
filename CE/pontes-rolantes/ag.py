#encoding: utf-8
import sys
import random
import json
import time
import datetime
import copy
from multiprocessing import Pool, cpu_count
from pontes import executa, cria_estagios, cria_pontes
from ordem_servico import gera_individuo

def calcula_fitness(individuo):
    return executa(cria_pontes(), cria_estagios(), copy.copy(individuo[0]))

POOL = None
DEBUG = '--debug' in sys.argv

# primeira dimensão da população: lista de indivíduos (individuos[0..100])
# segunda dimensão da população: (individuo, Fitness) (individuos[0..100][0..1900], individuos[0..100][1])
# terceira dimensão da população (dentro do indivíduo): transicao (individuos[0..100][0..1900][0])

def inicializa_populacao(n):
    if n <= 0:
        return []
    print 'Incializando {} indivíduos'.format(n)
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
            pai1 = random.choice(individuos[:20])
            pai2 = random.choice(individuos[:20])
        filho1 = []
        filho2 = []
        for pos in range(len(pai1[0])):
            if chance_pai1 > random.random():
                filho1.append(pai1[0][pos])
                filho2.append(pai2[0][pos])
            else:
                filho1.append(pai2[0][pos])
                filho2.append(pai1[0][pos])
        individuos.append([filho1, calcula_fitness([filho1])])
        individuos.append([filho2, calcula_fitness([filho2])])
    return individuos

def mutacao(individuos, chance_mutacao):
    qtd_cromossomos = len(individuos[0][0])
    posicao = random.randint(0, qtd_cromossomos-4)
    mutados = 0
    i = 0
    for i in range(len(individuos)):
        if chance_mutacao > random.random():
            mutados += 1
            posicao_cromossomos_mudados = []

            while posicao in posicao_cromossomos_mudados or not individuos[i][0][posicao].get('possiveis'):
                posicao = random.randint(0, qtd_cromossomos-4)
            individuo = individuos[i][0]
            ponte = individuo[posicao]['ponte']
            while ponte == individuo[posicao]['ponte']:
                individuo[posicao]['ponte'] = random.choice(individuo[posicao]['possiveis'])
            #if individuo[posicao+1]['ponte'] in individuo[posicao]['possiveis']:
            #    #if individuo[posicao+1]['ponte'] == individuo[posicao]['ponte']:
            #    #    individuo[posicao]['ponte'] = random.choice(individuo[posicao]['possiveis'])
            #    individuo[posicao]['ponte'], individuo[posicao+1]['ponte'] = individuo[posicao+1]['ponte'], individuo[posicao]['ponte'] 
            #elif individuo[posicao-1]['ponte'] in individuo[posicao]['possiveis']:
            #    #if individuo[posicao-1]['ponte'] == individuo[posicao]['ponte']:
            #    #    individuo[posicao]['ponte'] = random.choice(individuo[posicao]['possiveis'])
            #    individuo[posicao]['ponte'], individuo[posicao-1]['ponte'] = individuo[posicao-1]['ponte'], individuo[posicao]['ponte'] 
            #else:
            #    individuo[posicao]['ponte'] = random.choice(individuo[posicao]['possiveis'])
            posicao_cromossomos_mudados.append(posicao)

            fitness = calcula_fitness(individuos[i])
            if fitness > individuos[i][1]:
                print 'Mutando para pior ({}->{}) :('.format(individuos[i][1], fitness)
            elif fitness < individuos[i][1]:
                print 'Mutando para melhor ({}->{}) :)'.format(individuos[i][1], fitness)
            else:
                print 'Mutando para o mesmo ({}->{}) :|'.format(individuos[i][1], fitness)
            individuos[i][1] = fitness
    return individuos, mutados

now = lambda: datetime.datetime.now().time().strftime('%Hh%Mm%Ss')

def salva_execucao(geracao, inicio_exec, inicio, individuos, evolucao_execucao, mutados, melhor):
    fim = datetime.datetime.now()
    g = str(geracao).rjust(5, '0')
    print u'[G{}][{}] Pior,Melhor fitness da geração {},{}. Mutados: {}. Melhor geral: {}'.format(g, now(), individuos[-1][1], individuos[0][1], mutados, melhor[1])
    evolucao_execucao.append(((fim-inicio).total_seconds(), individuos[0]))
    with open('execucao-{hora}.json'.format(hora=inicio_exec), 'w') as arquivo:
        arquivo.write(json.dumps(evolucao_execucao))
    return evolucao_execucao

def selecao(individuos, N):
    return individuos[:N]

def ordena(individuos):
    return sorted(individuos, key=lambda k: k[1])

def menor(individuos):
    return ordena(individuos)[0][1]

def ag():
    N = 100
    inicio_exec = now()
    individuos = inicializa_populacao(N)
    evolucao_execucao = []
    melhor = ordena(individuos)[0]
    qtd_geracoes_sem_mudar = 0
    for geracao in range(100):
        inicio = datetime.datetime.now()
        individuos = cruzamento(individuos, 20)
        chance_mutacao = 0.05*qtd_geracoes_sem_mudar
        individuos, mutados = mutacao(individuos, chance_mutacao)
        individuos = ordena(individuos)
        if chance_mutacao > 0.3:
            #descarta metade da população e gera novas soluções
            individuos = individuos[:N/2]
            individuos = individuos + inicializa_populacao(N/2)
        if menor(individuos) > melhor[1]:
            individuos.append(melhor)
        individuos = ordena(individuos)
        individuos = selecao(individuos, N)
        individuos = ordena(individuos)
        if individuos[0][1] < melhor[1]:
            melhor = copy.copy(individuos[0])
            qtd_geracoes_sem_mudar = 0
        elif individuos[0][1] > melhor[1]:
            individuos.append(melhor)
            qtd_geracoes_sem_mudar += 1
        else:
            qtd_geracoes_sem_mudar += 1
        melhor = copy(individuos[0]) if individuos[0][1] < melhor[1] else melhor
        evolucao_execucao = salva_execucao(geracao, inicio_exec, inicio, individuos, evolucao_execucao, mutados, melhor)
        if qtd_geracoes_sem_mudar == 15:
            print u'Parando por falta de convergência'
    print 'Melhor fitness: {}'.format(melhor[1])

if __name__ == '__main__':
    for ex in range(30):
        ag()
