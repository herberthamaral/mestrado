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
        DADOS.extend(json.loads(open(filename).read()))

# converte para CSV
csv = ','.join(DADOS[0].keys()[1:])+'\n'
for d in DADOS:
    csv += ','.join([str(v) for v  in d.values()[1:]])+'\n'

with open('dados.csv', 'w') as f:
    f.write(csv)
