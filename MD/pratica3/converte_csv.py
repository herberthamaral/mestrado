# encoding: utf-8
"""
Converte os resultados parciais para csv
"""
import os
import json

# carrega os dados
DADOS = []
for i in range(100):
    filename = 'iteracao-{num}.json'.format(num=str(i).rjust(3, '0'))
    if os.path.exists(filename):
        dados = json.loads(open(filename).read())
        for d in dados:
            del d['matriz_confusao']
            DADOS.append(d)

# converte para CSV
csv_header = ','.join(DADOS[0].keys())+'\n'
csv_content = {}
for d in DADOS:
    key = d['dataset_file']+'-'+d['function_path']
    if key not in csv_content:
        csv_content[key] = csv_header
    csv_content[key] += ','.join([str(v) for v  in d.values()])+'\n'

for key,value in csv_content.items():
    with open(key+'.csv', 'w') as f:
        f.write(value)
