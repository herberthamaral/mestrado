# encoding: utf-8
# Extrai dados usados para o ANFIS. Uso:
#    python normalize.py entrada.csv saida.csv
#
# Sendo que o arquivo de entrada é um dos blocos do dataset baixado por
# download_dataset.sh

import sys
from collections import OrderedDict

input_file = sys.argv[1]
output_file = sys.argv[2]

csv_content = open(input_file, 'r').read().replace('?', '-1').split('\n')
csv_header = csv_content[0].replace('"', '').split(',')

parsed_csv = [linha.split(',') for linha in csv_content[1:]]
odata = []
for reg in parsed_csv:
    if len(reg) != 12:
        continue
    odata.append((reg[2], reg[4], str(float(reg[7])+float(reg[8])+float(reg[9])), str(int(reg[11]=='TRUE'))))

output_file_content = '\n'.join([','.join(line) for line in odata])
with open(output_file, 'w') as output:
     output.write(output_file_content)
