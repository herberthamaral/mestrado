# encoding: utf-8
import os
import json
import math
import numpy as np
from collections import OrderedDict
import matplotlib.lines as mlines
import matplotlib.pyplot as plt

arquivos_execucoes = [ex for ex in os.listdir('.') if ex.endswith('.json')]
fitness_execucoes = []
tempo_processamento_execucoes = []
motivos_parada = []
for a in arquivos_execucoes:
    with open(a, 'r') as arquivo_execucao:
        conteudo = arquivo_execucao.read()
        conteudo_parseado = json.loads(conteudo)
        fitnesses = [c[1][1] for c in conteudo_parseado]
        tempos = [c[0] for c in conteudo_parseado]
        motivo_parada = u'Num. máximo de gerações' if len(fitnesses) == 100 else u'Convergência prematura'
        motivos_parada.append(motivo_parada)
        fitness_execucoes.append(fitnesses)
        tempo_processamento_execucoes.append(tempos)
fitness_execucoes = [fitness+[fitness[-1]]*(100-len(fitness)) for fitness in fitness_execucoes]
fitness_execucoes_com_label = [[{'geracao': i, 'fitness': f} for i,f in enumerate(fitness)] for fitness in fitness_execucoes]

media = lambda X: sum(X)/float(len(X))
variancia = lambda X: sum([(float(xi) - media(X))**2 for xi in X])/float(len(X))
desvio = lambda X: math.sqrt(variancia(X))
tsigma = lambda X: 2*desvio(X)/math.sqrt(len(X))


# boxplot dos fitness das execuções
fig = plt.figure(1, figsize=(9,6))
ax = fig.add_subplot(111)
bp = ax.boxplot(fitness_execucoes)
fig.savefig('fig1.png', bbox_inches='tight')
fig.clf()
# histograma dos fitness das execuções

# gráfico de decaimento do fitness das execuções
desvios = [tsigma([f[i] for f in fitness_execucoes]) for i, _ in enumerate(fitness_execucoes[0])]
medias = [media([f[i] for f in fitness_execucoes]) for i, _ in enumerate(fitness_execucoes[0])]
desvios_up = [medias[i]+desvios[i] for i, _ in enumerate(medias)]
desvios_down = [medias[i]-desvios[i] for i, _ in enumerate(medias)]
plt.title(u'Decaimento médio (com desvios-padrão) do fitness nas gerações')

plt.plot(range(len(desvios_up)), desvios_up, 'g.')
plt.plot(range(len(desvios_down)), desvios_down, 'g.')
plt.plot(range(len(medias)), medias, 'b')
legenda_media = mlines.Line2D([], [], color='blue', marker='', markersize=15, label=u'Média')
legenda_intervalo = mlines.Line2D([], [], color='green', marker='.', markersize=5, label=u'Intervalo de confiança')
plt.ylabel(u'Fitness')
plt.xlabel(u'Gerações')
plt.legend(handles=[legenda_media, legenda_intervalo])
plt.savefig('decaimento.png')

# tabela - tempo de processamento - média para cada geração (std), média por execução (std)
execucoes = []
for ex in tempo_processamento_execucoes:
    execucoes += ex
tabela_tempo_processamento = dict(
    media_geracao = media(execucoes),
    desvio_geracao = desvio(execucoes),
    media_execucao = sum(execucoes)/len(tempo_processamento_execucoes),
    desvio_execucao = desvio([sum(ex) for ex in tempo_processamento_execucoes])
)
print u' & '.join(tabela_tempo_processamento.keys())+'\\\\ \\hline'
print u' & '.join(map(unicode, tabela_tempo_processamento.values()))+'\\\\ \\hline'
print '-'*20
# tabela - média (std) do fitness amostrado a cada 10 gerações
media_fitness = [media([f[i] for f in fitness_execucoes]) for i in range(0, 100, 10)]
desvio_fitness = [desvio([f[i] for f in fitness_execucoes]) for i in range(0, 100, 10)]
print u'Geração & Média (desvio padrão) \\\\ \\hline'
for linha, posicao in enumerate(range(0,100, 10)):
    print ' & '.join([str(posicao+1), str(media_fitness[linha])+' ({}) '.format(desvio_fitness[linha])])+'\\\\ \\hline'
print '-'*20
# tabela - percentis de queda média em gerações - 80%, 90%, 95%, 99% (considerar
#   p=(maior-menor)*percentil e ver qual é a geração mais próxima de p). p80 diz
#   quantas gerações são necessárias para perceber 80% da queda do fitness.
posicao_mais_proxima = lambda valor, vetor: vetor.index(min([(abs(x - valor),x)  for x in vetor])[1])
media_alta = media([f[0] for f in fitness_execucoes])
media_baixa = media([f[-1] for f in fitness_execucoes])
p80 = (media_alta - media_baixa)*0.8
p90 = (media_alta - media_baixa)*0.9
p95 = (media_alta - media_baixa)*0.95
p99 = (media_alta - media_baixa)*0.99
percentis = OrderedDict(
    p80 = posicao_mais_proxima(media_alta-p80, sorted([media(f) for f in fitness_execucoes], reverse=True)),
    p90 = posicao_mais_proxima(media_alta-p90, sorted([media(f) for f in fitness_execucoes], reverse=True)),
    p95 = posicao_mais_proxima(media_alta-p95, sorted([media(f) for f in fitness_execucoes], reverse=True)),
    p99 = posicao_mais_proxima(media_alta-p99, sorted([media(f) for f in fitness_execucoes], reverse=True)),
)
print u' & '.join(percentis.keys())+'\\\\ \\hline'
print u' & '.join(map(unicode, percentis.values()))+'\\\\ \\hline'
