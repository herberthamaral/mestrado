# encoding: utf-8
import numpy as np

def load_dataset(filename):
    dataset = open(filename, 'r').read().split('\n')
    dataset = [[dado.strip() for indice, dado in enumerate(linha.split(','))] for linha in dataset if linha]
    dataset = np.array(dataset)
    return dataset

def save_dataset(dataset, filename):
    conteudo = '\n'.join([','.join([str(i) for i in linha]) for linha in dataset])
    with file(filename, 'w') as fp:
        fp.write(conteudo)
