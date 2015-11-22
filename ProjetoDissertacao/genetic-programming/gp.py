# encoding: utf-8
import random
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

def gen_random_tree(args):
    if len(args) == 1:
        return args[0]
    tree = [random.choice(fmap.keys())]
    leafes = [gen_random_tree(args[:len(args)/2]), gen_random_tree(args[len(args)/2:])]
    random.shuffle(leafes)
    tree.extend(leafes)
    return tree

DATASET = []

def fitness(ftree):
    global DATASET
    if not DATASET:
        linhas = unicode(open('dataset.csv').read()).split('\n')
        header = [l.strip() for l in linhas[0].split(',')]
        DATASET = [dict(zip(header, [l.strip() for l in linha.strip().split(',')])) for linha in linhas[1:] if linha]
    #todas comparações com jaro-winkler
    verdadeiro_positivo = 0
    verdadeiro_negativo = 0
    falso_positivo = 0
    falso_negativo = 0
    for linha1 in DATASET:
        for linha2 in DATASET:
            if linha1 == linha2:
                continue
            evidencias = {attr:jaro_winkler(linha1[attr], linha2[attr]) for attr in linha1.keys() if attr!='rec_id'}
            resultado = execute(ftree, evidencias)
            if mesmo_registro(linha1, linha2):
                if resultado <= 0.95:
                    falso_negativo += 1
                else:
                    verdadeiro_positivo += 1
            else:
                if resultado <= 0.95:
                    verdadeiro_negativo += 1
                else:
                    falso_positivo += 1
    precisao = verdadeiro_positivo/float(verdadeiro_positivo+falso_positivo)
    recall = verdadeiro_positivo/float(verdadeiro_positivo+falso_negativo)
    f1 = (2*precisao*recall)/(precisao+recall)
    return dict(f1=f1, precisao=precisao, recall=recall)

def mesmo_registro(reg1, reg2):
    return reg1['rec_id'].split('-')[1] == reg2['rec_id'].split('-')[1]

def mutate_tree(tree, attrs):
    rattrs = random.sample(attrs, random.randint(1, random.randint(1,len(attrs)/2)))
    random.shuffle(rattrs)
    random_subtree = gen_random_tree(rattrs)
    element_to_replace = random.randint(1, len(attrs))
    print 'element to replace', element_to_replace
    print 'random_subtree', random_subtree
    tree = replace_element(element_to_replace, tree, random_subtree)
    return tree

def replace_element(element, tree, random_subtree, current_element=0, path=[], orig_tree=[]):
    returntree = []
    returntree.append(tree[0] if type(tree)==list else tree)
    if type(tree) == list:
        for pos,el in enumerate(tree[1:]):
            current_element += 1
            r = replace_element(element, el, random_subtree, current_element)
            if element == current_element and type(r) == list:
                returntree.append(random_subtree)
            else:
                returntree.append(r)
    return returntree[0] if len(returntree) == 1 else returntree

if __name__=='__main__':
    attrs=['given_name','surname','street_number','address_1','address_2','suburb','postcode','state','date_of_birth','soc_sec_id']
    tree = gen_random_tree(attrs)
    print tree
    mutated = mutate_tree(tree, attrs)
    print tree == mutated
    print mutated
    #print fitness(tree)
