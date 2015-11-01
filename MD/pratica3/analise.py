# encoding: utf-8
"""
Análise dos dados coletados
Amostra dos dados:

 {
  "erro_str": "", 
  "erro": 0, 
  "tteste": 0.031165122985839844, 
  "precisao": 0.8325358851674641, 
  "ttreinamento": 0.009914159774780273, 
  "dataset_file": "abalone.data", 
  "function_path": "sklearn.linear_model.LinearRegression"
 } 
"""
import os
import json
from collections import OrderedDict
from scipy.stats import levene, kstest, normaltest, shapiro, anderson
from main import FUNCOES, DATASETS

# carrega os dados
DADOS = []
for i in range(100):
    filename = 'iteracao-{num}.json'.format(num=str(i).rjust(3, '0'))
    if os.path.exists(filename):
        DADOS.extend(json.loads(open(filename).read()))

# converte para CSV
csv = ','.join(DADOS[0].keys()[1:])+'\n'
for d in DADOS:
    csv += ','.join([str(v) for v  in d.values()[1:]])+'\n'

with open('dados.csv', 'w') as f:
    f.write(csv)

# testa normalidade da precisao
#precisao = [d['precisao'] for d in DADOS if d['function_path']==FUNCOES[6] and d['erro'] == 0] 
#print kstest(precisao, 'norm')
#print normaltest(precisao)
#print shapiro(precisao)
#print anderson(precisao)
