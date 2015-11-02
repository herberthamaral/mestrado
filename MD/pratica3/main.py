# encoding: utf-8
import sys
import time
import json
import warnings
import multiprocessing
from importlib import import_module
import numpy as np
from sklearn.cross_validation import KFold

# lazy load de datasets
LOADED_DATASETS = {}

def minmax(xi, maxx, minx):
    return (float(xi) - minx)/(float(maxx)-minx)

def minmax_array(x):
    maxx = max(x)
    minx = min(x)
    return [minmax(xi, maxx, minx) for xi in x]

DATASETS = [
    'abalone.data',
    'car.data',
    'banknote.data',
]

FUNCOES = [
    'sklearn.linear_model.SGDClassifier',
    'sklearn.linear_model.Perceptron',
    'sklearn.linear_model.PassiveAggressiveClassifier',
    'sklearn.lda.LDA',
    'sklearn.kernel_ridge.KernelRidge',
    'sklearn.svm.SVC',
    'sklearn.svm.NuSVC',
    'sklearn.svm.LinearSVC',
    'sklearn.linear_model.SGDClassifier',
    'sklearn.neighbors.RadiusNeighborsClassifier',
    'sklearn.neighbors.KNeighborsClassifier',
    'sklearn.naive_bayes.GaussianNB',
    'sklearn.naive_bayes.MultinomialNB',
    'sklearn.naive_bayes.BernoulliNB',
    'sklearn.tree.DecisionTreeClassifier',
    'sklearn.ensemble.GradientBoostingClassifier',
    'mlp.MLPClassifier',
]

def trata_datasets():
    # o dataset banknote não preicisa de tratamento
    with open('abalone.data', 'r+') as f:
        abalone = f.read()
        abalone = abalone.replace('I', '0')
        abalone = abalone.replace('M', '1')
        abalone = abalone.replace('F', '2')
        f.seek(0)
        f.write(abalone)
        f.truncate()
    with open('car.data', 'r+') as f:
        car = f.read()
        car = car.replace('more', '5')
        car = car.replace('vhigh', '3')
        car = car.replace('vgood', '3')
        car = car.replace('good', '2')
        car = car.replace('high', '2')
        car = car.replace('big', '2')
        car = car.replace('med', '1')
        car = car.replace('unacc', '0')
        car = car.replace('acc', '1')
        car = car.replace('low', '0')
        car = car.replace('small', '0')
        f.seek(0)
        f.write(car)
        f.truncate()

def load_dataset(filename, separator=','):
    if filename not in LOADED_DATASETS:
        LOADED_DATASETS[filename] = np.array([linha.split(separator) for linha in open(filename, 'r').read().split('\n') if linha.strip()]).astype(float)
    return LOADED_DATASETS[filename]

def load_function(function_path):
    module = '.'.join(function_path.split('.')[:-1])
    function_name = function_path.split('.')[-1]
    function = getattr(import_module(module), function_name)
    return function

def test_function(kwargs):
    kwargs = dict(kwargs)
    function_path = kwargs['function_path']
    dataset_file =  kwargs['dataset_file']
    train_indexes = kwargs.pop('train_indexes')
    test_indexes =  kwargs.pop('test_indexes')
    classes_possiveis = kwargs['classes_possiveis']
    """
    Exemplo: 
    test_function('svm.SVC', 'abalone.data', kftrain, kftest)

    Retorno:
    (1.2, 0.2, 0.94) => 1.2 segundos para treinar, 0.2 para testar e 94% de precisão
    """
    function = load_function(function_path)
    dataset = load_dataset(dataset_file)
    num_linhas_dataset = len(dataset)
    num_colunas_dataset = len(dataset[0])

    #Retorna todas menos a última coluna. 
    #Veja referência http://docs.scipy.org/doc/numpy/reference/arrays.indexing.html
    _ = dataset[:,:-1]
    x = [minmax_array(_[i]) for i in train_indexes]
    x_teste = [minmax_array(_[i]) for i in test_indexes]

    # pega somente a última coluna
    _ = dataset.T[-1] 
    y = [_[i] for i in train_indexes]
    y_teste = [_[i] for i in test_indexes]

    instancia = function()
    t0 = time.time()
    erro=0
    erro_str = ''
    try:
        instancia.fit(x, y)
    except Exception, e:
        erro_str = str(e)
        erro=1
    t1 = time.time()
    ttreinamento = t1-t0

    t0 = time.time()
    erros = 0
    #classes_possiveis = sorted(list(set(y_teste)))
    matriz_confusao = [[0 for i in classes_possiveis] for j in classes_possiveis]
    if not erro:
        for i,xt in enumerate(x_teste):
            try:
                predicao = round(instancia.predict(xt)[0])
                indice_certo = classes_possiveis.index(y_teste[i])
                if predicao != y_teste[i]:
                    try:
                        indice_incorreto = classes_possiveis.index(predicao)
                        matriz_confusao[indice_incorreto][indice_certo] += 1
                    except ValueError:
                        # classificou como uma outra classe qualquer
                        pass
                    erros += 1
                else:
                    matriz_confusao[indice_certo][indice_certo] += 1

            except:
                erros += 1
    else:
        erros = len(y_teste)
    precisao = (len(y_teste) - erros)/float(len(y_teste))
    t1 = time.time()
    tteste = t1-t0
    resultado = dict(ttreinamento=ttreinamento,
                     tteste=tteste,
                     precisao=precisao,
                     num_erros=erros,
                     foldsize=len(y_teste),
                     erro=erro,
                     erro_str=erro_str,
                     matriz_confusao=matriz_confusao)
    resultado.update(kwargs)
    return resultado.items()

def reporta_resultado(num_iteracao, resultado):
    filename = "iteracao-{num_iteracao}.json".format(num_iteracao=str(num_iteracao).rjust(3, '0'))
    resultado = [dict(r) for r in resultado]
    resultado = merge_dados_resultado(resultado)
    with open(filename, 'w') as f:
        f.write(json.dumps(resultado, indent=1))

def merge_dados_resultado(resultado):
    merged = []
    for k,d in enumerate(DATASETS):
        for i,f in enumerate(FUNCOES):
            tmp = {}
            for j in range(10):
                indice = (k+1)*(i+1)+j
                resultado_dict = dict(resultado[indice])
                tmp['tteste'] = resultado_dict['tteste'] + tmp.get('tteste', 0)
                tmp['ttreinamento'] = resultado_dict['ttreinamento'] + tmp.get('ttreinamento', 0)
                tmp['dataset_file'] = resultado_dict['dataset_file']
                tmp['function_path'] = resultado_dict['function_path']
                matriz = np.array(resultado_dict['matriz_confusao'])
                try:
                    tmp['matriz_confusao'] = matriz + np.array(tmp['matriz_confusao']) if tmp.get('matriz_confusao', None) is not None else matriz
                except:
                    import pdb;pdb.set_trace()
                tmp['matriz_confusao'] = [list(l) for l in tmp['matriz_confusao']]
                tmp['num_erros'] = resultado_dict['num_erros'] + tmp['num_erros'] if tmp.get('num_erros') else resultado_dict['num_erros']
                tmp['tamanho_dataset'] = resultado_dict['foldsize'] + tmp['tamanho_dataset'] if tmp.get('tamanho_dataset') else resultado_dict['foldsize']
            tmp['precisao'] = (float(tmp['tamanho_dataset'])-tmp['num_erros'])/tmp['tamanho_dataset']
            merged.append(tmp)
    return merged

if __name__ == '__main__':
    trata_datasets()
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    for num_execucao in range(100):
        list_args = []
        for dataset in DATASETS:
            N = len(load_dataset(dataset))
            kf = list(KFold(n=N, n_folds=10))
            classes_possiveis = sorted(list(set((load_dataset(dataset).T[-1]))))
            for funcao in FUNCOES:
                for trainset, testset in kf:
                    kwargs = dict(function_path=funcao,
                                  dataset_file=dataset,
                                  train_indexes=list(trainset),
                                  test_indexes=list(testset),
                                  classes_possiveis=classes_possiveis)
                    list_args.append(kwargs.items())

        #resultado = []
        #for args in list_args:
        #    resultado.append(test_function(args))
        #reporta_resultado(num_execucao, resultado)
        resultado = pool.map(test_function, list_args)
        resultado = [dict(r) for r in resultado]
        reporta_resultado(num_execucao, resultado)
        sys.stdout.write('.')
        sys.stdout.flush()
