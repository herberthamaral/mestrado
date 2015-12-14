# encoding: utf-8
import sys
from collections import OrderedDict
TEMPOS_DESLOCAMENTO = OrderedDict([
    ('CV1',{ 'RH': 10, 'FP': 15, 'LC': 15, 'CC': 10, 'BO': 10, },),
    ('CV2',{ 'RH': 10, 'FP': 15, 'LC': 15, 'CC': 10, 'BO': 10, },),
    ('RH' ,{ 'CV': 10, 'FP': 10, 'LC': 15, 'CC': 15, },),
    ('FP' ,{ 'CV': 15, 'RH': 10, 'LC': 15, 'CC': 10, },),
    ('LC' ,{ 'CV': 15, 'RH': 15, 'FP': 15, },),
    ('CC' ,{ 'BO': 6, 'CV': 10, 'FP': 10, 'RH': 15, },),
    ('BO' ,{ 'CV': 10, 'CC': 6},),
])

POSICOES = {
        'CV1': 'esquerda',
        'CV2': 'esquerda',
        'RH' : 'centro',
        'FP' : 'centro',
        'LC' : 'direita',
        'CC' : 'direita',
        'BO' : 'centro',
}

TEMPOS_EXECUCAO = {
    'CV1': 38, 'RH': '25', 'FP': 45, 'BO': 20, 
    'CV2': 38, 'RH': '25', 'FP': 45, 'BO': 20, 
    'LC': {'A': 34, 'B': 34, 'C': 32},
    'CC':{'D': 75, 'E': 75, 'F': 70, 'G': 80, 'H': 65, 'I': 75, 'J': 70, 'K': 80, 'L': 30},
}

pontes = {
        'A': {'origem': None, 'destino': None, 'os': None, 'tempo_restante': 0, 'status': 'parada', 'estagio': 'CV1', 'intuito_de_pegar': None},
        'B': {'origem': None, 'destino': None, 'os': None, 'tempo_restante': 0, 'status': 'parada', 'estagio': 'CV1', 'intuito_de_pegar': None},
        'C': {'origem': None, 'destino': None, 'os': None, 'tempo_restante': 0, 'status': 'parada', 'estagio': 'FP', 'intuito_de_pegar': None},
}
estagios = {
        'CV1': {'os': None,'tempo_restante': 0, 'nome': 'CV1', 'status':'parado'}, 
        'CV2': {'os': None,'tempo_restante': 0, 'nome': 'CV2', 'status':'parado'},
        'FP':  {'os': None,'tempo_restante': 0, 'nome': 'FP',  'status':'parado'},
        'LC':  {'os': None,'tempo_restante': 0, 'nome': 'LC',  'status':'parado'},
        'CC':  {'os': None,'tempo_restante': 0, 'nome': 'CC',  'status':'parado'},
}


def em_producao(os, estagios):
    return any([e['os'] == os for e in estagios and e['status']=='processando'])

def pronto(os, estagios):
    return any([e['os'] == os for e in estagios and e['status']=='parado'])

def existe_os_em_processamento(estagios):
    return any([estagios[nome]['status'] == 'processando' for nome in estagios.keys() if estagios[nome]['os']])

def existe_ponte_em_movimentacao(pontes):
    return any([pontes[p]['status'] == 'transportando' for p in pontes.keys()])

def tick(estagios, pontes, debug=False):
    for e in estagios.keys():
        if estagios[e]['status'] == 'processando':
            estagios[e]['tempo_restante'] -= 1
            if estagios[e]['tempo_restante'] == 0:
                estagios[e]['status'] = 'parado'
                log('Fim do processamento da O.S {os} no estagio {estagio}'.format(os=estagios[e]['os'][0], estagio=e), debug)
    for p in pontes.keys():
        estagio_da_os = filter(lambda k: estagios[k]['os'] == (400011, 'A'), estagios.keys())
        if pontes[p]['status'] == 'transportando':
            pontes[p]['tempo_restante'] -= 1
            if pontes[p]['tempo_restante'] == 0:
                if pontes[p]['os']:
                    kwargs = dict(os=pontes[p]['os'][0], estagio=pontes[p]['destino'], ponte=p)
                    log('Fim da movimentação da ponte {ponte} com O.S {os} para o estagio {estagio}'.format(**kwargs), debug)
                    log('Adiciona OS {os} em {destino}'.format(os=pontes[p]['os'][0], destino=pontes[p]['destino']), debug)
                    estagios[pontes[p]['destino']]['os'] = pontes[p]['os']
                    estagios[pontes[p]['destino']]['tempo_restante'] = TEMPOS_EXECUCAO[estagios[pontes[p]['destino']]['nome']]
                    if type(estagios[pontes[p]['destino']]['tempo_restante']) == dict:
                        estagios[pontes[p]['destino']]['tempo_restante'] = estagios[pontes[p]['destino']]['tempo_restante'][pontes[p]['os'][1]]
                    estagios[pontes[p]['destino']]['status'] = 'processando'
                else:
                    kwargs = dict(estagio=pontes[p]['destino'], ponte=p)
                    log('Fim da movimentação da ponte {ponte} vazia para o estagio {estagio}'.format(**kwargs), debug)
                pontes[p]['estagio'] = pontes[p]['destino']
                pontes[p]['origem'] = pontes[p]['destino'] = pontes[p]['os'] = None
                pontes[p]['status'] = 'parada'

pontes_a_esquerda = lambda ponte: {'A': [], 'B': ['A'], 'C':['A', 'B']}[ponte]
pontes_a_direita  = lambda ponte: {'A': ['B', 'C'], 'B': ['C'], 'C':[]}[ponte]

def sentido_movimentacao(ponte, destino):
    origem = POSICOES[ponte['estagio']]
    destino = POSICOES[destino]
    if origem != destino:
        if origem == 'esquerda':
            return 'direita'
        if origem == 'direita':
            return 'esquerda'
        if origem == 'centro':
            return destino
    return ''

def pontes_no_caminho(ponte, destino, pontes):
    if pontes[ponte]['estagio'] == destino and pontes[ponte]['status'] == 'parada':
        return []
    if sentido_movimentacao(pontes[ponte], destino) == 'direita':
        if ponte == 'C':
            return []
        elif ponte == 'B':
            if POSICOES[pontes['C']['estagio']] == 'direita':
                return []
            elif POSICOES[pontes['C']['estagio']] == 'centro' and POSICOES[destino] == 'direita':
                return ['C']
        elif ponte == 'A':
            if POSICOES[destino] == 'esquerda':
                return []
            elif POSICOES[destino] == 'direita':
                meio = ('esquerda', 'centro')
                caminho = []
                if POSICOES[pontes['B']['estagio']] in meio:
                    caminho.append('B')
                if POSICOES[pontes['C']['estagio']] in meio:
                    caminho.append('C')
                return caminho
            elif POSICOES[destino] == 'centro':
                if POSICOES[pontes['B']['estagio']] == 'esquerda':
                    return ['B']
    elif sentido_movimentacao(pontes[ponte], destino) == 'esquerda':
        if ponte == 'A':
            return []
        elif ponte == 'B':
            if POSICOES[pontes['A']['estagio']] == 'esquerda':
                return []
            elif POSICOES[pontes['A']['estagio']] in ('centro', 'direita') and POSICOES[pontes['B']['estagio']] in ('centro', 'direita'):
                return ['A']
        elif ponte == 'C':
            caminho = []
            if POSICOES[destino] == 'centro':
                if POSICOES[pontes['B']['estagio']] == 'direita':
                    caminho.append('B')
            return caminho
    return []

def movimenta_se_possivel(ponte, destino, pontes, debug=False):
    caminho = pontes_no_caminho(ponte, destino, pontes)
    if caminho:
        movimenta_se_possivel(caminho[0], destino, pontes, debug)
    if pontes[ponte]['status'] == 'parada':
        pontes[ponte]['status'] = 'transportando'
        pontes[ponte]['origem'] = pontes[ponte]['estagio']
        pontes[ponte]['destino'] = destino
        try:
            log('Movimentando ponte {ponte} vazia para {destino}'.format(**locals()), debug)
            pontes[ponte]['tempo_restante'] = TEMPOS_DESLOCAMENTO[pontes[ponte]['origem']][pontes[ponte]['destino']]/2
        except:
            log('Movimentando ponte {ponte} para {destino} através do deslocamento para CV1'.format(**locals()), debug)
            pontes[ponte]['destino'] = 'CV1' 
            pontes[ponte]['tempo_restante'] = TEMPOS_DESLOCAMENTO[pontes[ponte]['origem']]['CV']/2


def log(msg, debug=False):
    if debug:
        print msg

def executa(pontes, estagios, transicoes, debug=False):
    tempo_total = 0
    qtd_transicoes = len(transicoes)
    iteracoes_com_mesmo_numero_de_transicoes = 0
    while len(transicoes) > 0:
        remover = []
        if qtd_transicoes == len(transicoes):
            iteracoes_com_mesmo_numero_de_transicoes += 1
        else:
            iteracoes_com_mesmo_numero_de_transicoes = 0
            qtd_transicoes = len(transicoes)

        if iteracoes_com_mesmo_numero_de_transicoes == 10:
            print u'Parado há mais de 10 iterações'
            iteracoes_com_mesmo_numero_de_transicoes = 0
            for p in pontes.keys():
                pontes[p]['intuito_de_pegar'] = None
        for t in transicoes:
            if t['origem'] is None and estagios[t['destino']]['os'] is None: #entrada de O.S na aciaria
                estagios[t['destino']]['os'] = t['os']
                estagios[t['destino']]['tempo_restante'] = TEMPOS_EXECUCAO[estagios[t['destino']]['nome']]
                estagios[t['destino']]['status'] = 'processando'
                log('Adiciona OS {os} em {destino}'.format(os=t['os'][0], destino=t['destino']), debug)
                remover.append(t)
            if t['destino'] is None and estagios[t['origem']]['os'] is not None: #saída de O.S da aciaria
                estagios[t['origem']]['os'] = None
                remover.append(t)
            if t['origem'] is not None and estagios[t['origem']]['os'] and estagios[t['origem']]['status'] == 'parado': #'meio de campo' da aciaria
                if pontes[t['ponte']]['status'] == 'parada' and \
                   pontes[t['ponte']]['estagio'][:2] == t['origem'][:2] and \
                   t['os'] == estagios[t['origem']]['os'] and\
                   not estagios[t['destino']]['os']:
                    caminho = pontes_no_caminho(t['ponte'], t['destino'], pontes)
                    if caminho:
                        movimenta_se_possivel(caminho[0], t['destino'], pontes, debug)
                    else:
                        if not pontes[t['ponte']]['intuito_de_pegar'] or pontes[t['ponte']]['intuito_de_pegar'] == t['os']:
                            pontes[t['ponte']]['status'] = 'transportando'
                            pontes[t['ponte']]['os'] = t['os']
                            pontes[t['ponte']]['origem'] = t['origem']
                            pontes[t['ponte']]['destino'] = t['destino']
                            pontes[t['ponte']]['tempo_restante'] = TEMPOS_DESLOCAMENTO[t['origem']][t['destino']]
                            pontes[t['ponte']]['intuito_de_pegar'] = None
                            kwargs = dict(os=t['os'][0], origem=t['origem'], ponte=t['ponte'], destino=t['destino'])
                            log('Pega OS {os} em {origem} com ponte {ponte} para levar para {destino}'.format(**kwargs), debug)
                            estagios[t['origem']]['os'] = None
                            remover.append(t)
                if pontes[t['ponte']]['status'] == 'parada' and pontes[t['ponte']]['estagio'][:2] != t['origem'][:2] and not pontes[t['ponte']]['os']:
                    caminho = pontes_no_caminho(t['ponte'], t['destino'], pontes)
                    if caminho:
                        movimenta_se_possivel(caminho[0], t['destino'], pontes, debug)
                    elif not pontes[t['ponte']]['intuito_de_pegar']:
                        pontes[t['ponte']]['status'] = 'transportando'
                        pontes[t['ponte']]['os'] = None
                        pontes[t['ponte']]['origem'] = pontes[t['ponte']]['estagio']
                        pontes[t['ponte']]['destino'] = t['origem']
                        pontes[t['ponte']]['tempo_restante'] = TEMPOS_DESLOCAMENTO[t['origem']][t['destino']]/2
                        pontes[t['ponte']]['intuito_de_pegar'] = t['os']
                        kwargs = dict(ponte=t['ponte'], destino=t['origem'], os=t['os'][0], origem=pontes[t['ponte']]['estagio'])
                        log('Movimenta ponte {ponte} vazia de {origem} para {destino} para pegar O.S {os}'.format(**kwargs), debug)

        while existe_os_em_processamento(estagios) or existe_ponte_em_movimentacao(pontes):
            tick(estagios, pontes, debug)
            tempo_total += 1
        [transicoes.remove(v) for v in remover if v in transicoes]
    return tempo_total


if __name__ == '__main__':
    import random
    transicoes = [
            {'origem': None,  'destino': 'CV1', 'os': [1, 'A'], 'ponte': 'B'},
            {'origem': None,  'destino': 'CV2', 'os': [2, 'A'], 'ponte': 'B'},
            {'origem': 'CV1', 'destino': 'FP',  'os': [1, 'A'], 'ponte': 'B'},
            {'origem': 'FP',  'destino': 'LC',  'os': [1, 'A'], 'ponte': 'B'},
            {'origem': 'CV2', 'destino': 'FP',  'os': [2, 'A'], 'ponte': 'B'},
            {'origem': 'FP',  'destino': 'LC',  'os': [2, 'A'], 'ponte': 'B'},
            {'origem': 'LC',  'destino': None,  'os': [2, 'A'], 'ponte': 'B'},
            {'origem': 'LC',  'destino': None,  'os': [1, 'A'], 'ponte': 'B'},
    ]
    random.shuffle(transicoes)
    print executa(pontes, estagios, transicoes, debug=True), 'minutos'
