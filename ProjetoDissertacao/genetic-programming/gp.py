# encoding: utf-8
import sys
import time
import copy
import random
import datetime
import json
import multiprocessing
from jellyfish import jaro_winkler

fmap = {
    '+': lambda *args: sum(args),
    '-': lambda x,y: x-y,
    '*': lambda x,y: x*y,
    #'/': lambda x,y: x/y,
    #'val': lambda: random.uniform(1,9)
}
def execute(ftree, kwargs={}):
    if type(ftree) in (int, float):
        return ftree
    if type(ftree) in (str, unicode):
        return kwargs[ftree]
    if len(ftree) in [0,1]:
        if kwargs:
            return kwargs.values()[0]
        return None if not ftree else ftree[0]

    f = ftree[0]
    fargs = [execute(arg, kwargs) for arg in ftree[1:]]
    return fmap[f](*fargs)

def optimize_tree(tree):
    if type(tree) != list:
        return tree
    if tree[0] == '-' and tree[1] == tree[2]:
        return 0
    if tree[0] == '+' and 0 in tree[1:]:
        return tree[1] if tree[1] !=0 else tree[2]
    if all([type(t) == float for t in tree[1:]]):
        return execute(tree)
    return [tree[0], optimize_tree(tree[1]), optimize_tree(tree[2])]

def gen_random_tree(args):
    if len(args) == 1:
        return args[0]
    tree = [random.choice(fmap.keys())]
    if random.random() > 0.8:
        args.append(random.uniform(1,9))
    left = gen_random_tree(args[len(args)/2:])
    right = gen_random_tree(args[:len(args)/2])
    leafes = [left, right]
    random.shuffle(leafes)
    tree.extend(leafes)
    return tree

DATASET = []

def fitness(individuo):
    ftree = individuo['tree']
    global DATASET
    if not DATASET:
        linhas = unicode(open('out.csv').read()).split('\n')
        header = [l.strip() for l in linhas[0].split(',')]
        DATASET = [dict(zip(header, [l.strip() for l in linha.strip().split(',')])) for linha in linhas[1:] if linha]
    #todas comparações com jaro-winkler
    verdadeiro_positivo = 0
    verdadeiro_negativo = 0
    falso_positivo = 0
    falso_negativo = 0
    for l1 in xrange(len(DATASET)):
        for l2 in xrange(l1+1, len(DATASET)):
            linha1, linha2 = DATASET[l1], DATASET[l2]
            if linha1 == linha2:
                continue
            evidencias = {}
            for attr in linha1.keys():
                if attr != 'rec_id':
                    evidencias[attr] = get_evidencia(linha1, linha2, attr)
            try:
                resultado = execute(ftree, evidencias)
            except Exception, e:
                resultado = 0
            if resultado >= 0.95:
                if mesmo_registro(linha1, linha2):
                    verdadeiro_positivo += 1
                else:
                    falso_positivo += 1
            else:
                if mesmo_registro(linha1, linha2):
                    falso_negativo += 1
                else:
                    verdadeiro_negativo += 1
    try:
        precisao = verdadeiro_positivo/float(verdadeiro_positivo+falso_positivo)
        recall = verdadeiro_positivo/float(verdadeiro_positivo+falso_negativo)
        f1 = (2*precisao*recall)/(precisao+recall)
    except ZeroDivisionError:
        f1 = 0
    print datetime.datetime.now(), f1
    return dict(tree=ftree, fitness=f1)

def get_evidencia(linha1, linha2, attr):
    return jaro_winkler(linha1[attr], linha2[attr])

def mesmo_registro(reg1, reg2):
    return reg1['rec_id'].split('-')[1] == reg2['rec_id'].split('-')[1]

def mutate_tree(tree, attrs):
    rattrs = random.sample(attrs, random.randint(1, random.randint(1,len(attrs)/2)))
    random_subtree = 0
    while random_subtree == 0:
        random.shuffle(rattrs)
        random_subtree = gen_random_tree(rattrs)
        random_subtree = poda({'tree':random_subtree, 'fitness': None})['tree']

    element_to_replace = random.randint(1, len(attrs))
    replace_element_bfs(element_to_replace, tree, random_subtree)
    print u'sub-árvore de mutação:', random_subtree
    return tree

def replace_element_bfs(element_num, tree, random_subtree):
    queue = []
    index = 0
    for el in tree[1:]:
        index += 1
        queue.append(el)
    while queue != []:
        element = queue[0]
        queue = queue[1:]
        if type(element) == list:
            for i, el in enumerate(element[1:]):
                index += 1
                queue.append(el)
                if index == element_num:
                    element[i+1] = random_subtree

def crossover(pares):
    filhos = []
    for par in pares:
        tree1, tree2 = par
        tree1, tree2 = tree1['tree'], tree2['tree']
        subtree1, subtree2 = None, None
        while not all([subtree1, subtree2]):
            ponto_corte1 = random.randint(1, len(plain(tree1)))
            ponto_corte2 = random.randint(1, len(plain(tree2)))
            subtree1 = get_element_by_pos(tree1 , ponto_corte1)
            subtree2 = get_element_by_pos(tree2, ponto_corte2)
        filho1 = copy.deepcopy(tree1)
        filho2 = copy.deepcopy(tree2)
        replace_element_bfs(ponto_corte1, filho1, subtree2)
        replace_element_bfs(ponto_corte2, filho2, subtree1)
        filhos.append({'tree':filho1, 'fitness': None})
        filhos.append({'tree':filho2, 'fitness': None})
    return filhos

def plain(tree):
    plained = []
    for el in tree:
        if type(el) == list:
            plained.extend(plain(el))
        else:
            plained.append(el)
    return plained

def get_element_by_pos(tree, pos):
    queue = []
    index = 0
    for el in tree[1:]:
        index += 1
        queue.append(el)
    while queue != []:
        element = queue[0]
        queue = queue[1:]
        if type(element) == list:
            for i, el in enumerate(element[1:]):
                index += 1
                queue.append(el)
                if index == pos:
                    return element[i+1]

def selecao_pais(pop, qtd_pares=6):
    pares = []
    pop = sorted(pop)[::-1]
    sum_fitness = float(sum([i['fitness'] for i in pop]))
    prob_acumulada = 0
    while len(pares) != qtd_pares:
        pais = []
        rand = random.random()
        while len(pais) != 2:
            for p in pop:
                prob_acumulada += p['fitness']/sum_fitness
                if prob_acumulada > rand and p not in pais:
                    pais.append(p)
                    break
        pares.append(pais)
    return pares


def init_pop(qtd, attrs, multi, calc_fitness=True):
    if qtd <= 0:
        return []
    print "Inicializando {} novos individuos".format(qtd)
    individuos = [{'tree': gen_random_tree(attrs), 'fitness': None} for i in range(qtd)]
    if calc_fitness:
        individuos = calcula_fitness_pop(individuos, multi)
    return individuos

POOL = None #evita leak de processos

def calcula_fitness_pop(individuos, multi=True):
    global POOL
    a_calcular = []
    for individuo in individuos:
        if individuo['fitness'] is None:
            a_calcular.append(individuo)
    individuos = [i for i in individuos if i['fitness'] is not None]
    if multi:
        if not POOL:
            POOL = multiprocessing.Pool(multiprocessing.cpu_count())
        individuos.extend(POOL.map(fitness, a_calcular))
    else:
        individuos.extend([fitness(a) for a in a_calcular])
    individuos = sorted(individuos)
    return individuos

def mutacao(pop, attrs, taxa=0.2):
    for p in pop:
        if taxa >= random.random():
            p['tree'] = mutate_tree(p['tree'], attrs)
            p['fitness'] = None
    return pop

def poda(individuo):
    podado = []
    individuo['tree'] = optimize_tree(individuo['tree'])
    while podado != individuo['tree']:
        podado = copy.copy(individuo['tree'])
        individuo['tree'] = optimize_tree(individuo['tree'])
    return individuo

def salva_resultado_arquivo(pop, geracao, ts):
    filename = 'exec-{ts}-geracao-{geracao}.json'.format(**locals())
    with open(filename, 'w') as f:
        f.write(json.dumps(pop))

def pg(multi=True, qtd_populacao=60):
    attrs=['given_name','surname','street_number','address_1','address_2','suburb','postcode','state','date_of_birth','soc_sec_id']
    for ex in range(1):
        print u"Inicializando geração ",ex+1
        pop = init_pop(qtd_populacao, attrs, multi)
        for i in range(20):
            pais = selecao_pais(pop)
            filhos = crossover(pais)
            filhos = mutacao(filhos, attrs)
            pop.extend(filhos)
            pop = calcula_fitness_pop(pop, multi)
            unique_individuals = []
            [unique_individuals.append(p) for p in pop if p not in unique_individuals] # não dá para usar set() aqui - listas não são hasheáveis
            pop.extend(init_pop(qtd_populacao-len(pop), attrs, multi))
            pop = calcula_fitness_pop(pop, multi)
            pop = sorted(pop)[::-1][:qtd_populacao]
            pop = [poda(p) for p in pop]
            print u'\nMelhor fitness da geração ',(i+1), pop[0]['fitness']
            print u'\nMelhor indivíduo:', pop[0]['tree']
            print u'\nMelhor indivíduo (plain):', plain(pop[0]['tree'])
            salva_resultado_arquivo(pop, i, str(ex).rjust(2, '0'))

if __name__=='__main__':
    pg(multi=True)
