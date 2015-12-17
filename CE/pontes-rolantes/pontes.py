# encoding: utf-8
import sys
from copy import copy

DEBUG = '--debug' in sys.argv

def tempo_deslocamento(origem, destino):
    origem, destino = origem[:2], destino[:2]
    tempos = dict([
        ('CV',{ 'RH': 10, 'FP': 15, 'CL': 15, 'CC': 10, 'BO': 10, },),
        ('RH', { 'CV': 10, 'FP': 10, 'CL': 15, 'CC': 15, },),
        ('FP',{ 'CV': 15, 'CV': 15, 'RH': 10, 'CL': 15, 'CC': 10, },),
        ('CL',{ 'CV': 15, 'RH': 15, 'FP': 15, },),
        ('CC',{ 'BO': 6, 'CV': 10, 'FP': 10, 'RH': 15, },),
        ('BO',{ 'CV': 10, 'CC': 6},),
    ])
    return tempos[origem][destino]

def posicao(estagio):
    estagio = estagio[:2]
    posicoes = {
            'CV': 0,
            'RH' : 5,
            'FP' : 10,
            'CL' : 20,
            'CC' : 20,
            'BO' : 10,
    }
    return posicoes[estagio]

def tempo_execucao(estagio, aco=''):
    estagio = estagio[:2]
    tempos = {
        'CV': 38, 'RH': 25, 'FP': 45, 'BO': 20, 
        'CL': {'A': 34, 'B': 34, 'C': 32, 'F':70, 'M': 0, 'N': 0, 'O': 0}, # Add: M=N=O=0min
        'CC':{ 'A': 34, 'B': 34, 'C': 32,'D': 75, 'E': 75, 'F': 70, 'G': 80, 'H': 65, 'I': 75, 'J': 70, 'K': 80, 'L': 30, 'M': 0, 'N':0, 'O':0}, # Add M=N=O=0m
    }
    return tempos[estagio][aco] if type(tempos[estagio]) == dict else tempos[estagio]

pontes = {
        'A': {'destino': None, 'os': None, 'tempo_restante': 0, 'status': 'parada', 'estagio': 'CV01', 'intuito_de_pegar': None},
        'B': {'destino': None, 'os': None, 'tempo_restante': 0, 'status': 'parada', 'estagio': 'CV01', 'intuito_de_pegar': None},
        'C': {'destino': None, 'os': None, 'tempo_restante': 0, 'status': 'parada', 'estagio': 'FPA01', 'intuito_de_pegar': None},
}

def cria_estagios():
    _estagios = {
            'CV': {'os': None,'tempo_restante': 0, 'status':'parado', 'aguardando': None}, 
            'FP': {'os': None,'tempo_restante': 0, 'status':'parado', 'aguardando': None},
            'RH': {'os': None,'tempo_restante': 0, 'status':'parado', 'aguardando': None},
            'CL': {'os': None,'tempo_restante': 0, 'status':'parado', 'aguardando': None},
            'CC': {'os': None,'tempo_restante': 0, 'status':'parado', 'aguardando': None},
    }
    estagios = dict()
    estagios['CV01'] = copy(_estagios['CV'])
    estagios['CV02'] = copy(_estagios['CV'])
    estagios['RH01'] = copy(_estagios['RH'])
    estagios['FPA01'] = copy(_estagios['FP'])
    estagios['FPA02'] = copy(_estagios['FP'])
    estagios['CC01'] = copy(_estagios['CC'])
    estagios['CC02'] = copy(_estagios['CC'])
    estagios['CL03'] = copy(_estagios['CL'])
    estagios['CL11'] = copy(_estagios['CL'])
    estagios['CL15'] = copy(_estagios['CL'])
    estagios['CL21'] = copy(_estagios['CL'])
    return estagios

estagios = cria_estagios()

def em_producao(os, estagios):
    return any([e['os'] == os for e in estagios and e['status']=='processando'])

def pronto(os, estagios):
    return any([e['os'] == os for e in estagios and e['status']=='parado'])

def existe_os_em_processamento(estagios):
    return any([estagios[nome]['status'] == 'processando' for nome in estagios.keys() if estagios[nome]['os']])

def existe_ponte_em_movimentacao(pontes):
    return any([pontes[p]['status'] == 'transportando' for p in pontes.keys()])

def tick(estagios, pontes, incremento, tempo_total):
    for e in estagios.keys():
        if estagios[e]['status'] == 'processando':
            estagios[e]['tempo_restante'] -= incremento
    for p in pontes.keys():
        if pontes[p]['status'] == 'transportando':
            pontes[p]['tempo_restante'] -= incremento

def sentido_movimentacao(ponte, destino):
    origem = posicao(ponte['estagio'])
    destino = posicao(destino)
    if origem < destino:
        return 'direita'
    elif origem > destino:
        return 'esquerda'
    return ''

def pontes_no_caminho(ponte, destino, pontes):
    incrementos = {'A': 0, 'B':1, 'C':2}
    meio = []
    if sentido_movimentacao(pontes[ponte], destino) == 'direita':
        meio = [p for p in pontes.keys()
                 if posicao(pontes[p]['estagio'])+incrementos[p] > posicao(pontes[ponte]['estagio'])+incrementos[ponte] and\
                    posicao(pontes[p]['estagio']) < posicao(destino)]
    elif sentido_movimentacao(pontes[ponte], destino) == 'esquerda':
        meio = [p for p in pontes.keys()
                 if posicao(pontes[p]['estagio'])+incrementos[p] < posicao(pontes[ponte]['estagio'])+incrementos[ponte] and\
                    posicao(pontes[p]['estagio']) > posicao(destino)]
    return sorted(meio)

def rota_colisao(ponte, destino, pontes):
    colisao = []
    if sentido_movimentacao(pontes[ponte], destino) == 'esquerda':
        colisao = [p for p in pontes 
                    if p < ponte and pontes[p]['status']=='transportando' and\
                       posicao(pontes[p]['destino']) > posicao(destino)]
    elif sentido_movimentacao(pontes[ponte], destino) == 'direita':
        colisao = [p for p in pontes 
                    if p > ponte and pontes[p]['status']=='transportando' and\
                       posicao(pontes[p]['destino']) < posicao(destino)]
    return colisao

def pontes_no_caminho_considerando_movimento(ponte, destino, pontes):
    no_caminho = pontes_no_caminho(ponte, destino, pontes)
    if not no_caminho:
        return []
    if sentido_movimentacao(pontes[ponte], destino) == 'direita':
        no_caminho = [p for p in no_caminho if p != ponte and \
                                            ((pontes[p]['status'] == 'transportando' and posicao(pontes[p]['destino']) < posicao(destino)) 
                                                or pontes[p]['status']=='parada')]
    elif sentido_movimentacao(pontes[ponte], destino) == 'esquerda':
        no_caminho = [p for p in no_caminho if p != ponte and \
                                            ((pontes[p]['status'] == 'transportando' and posicao(pontes[p]['destino']) > posicao(destino)) 
                                                or pontes[p]['status']=='parada')]
    return no_caminho
 
def ponte_pode_ser_movida_para_abrir_espaco(ponte, destino, pontes, estagios):
    no_caminho = pontes_no_caminho_considerando_movimento(ponte, destino, pontes)
    if not all([ponte_pode_ser_movida_para_abrir_espaco(p, destino, pontes, estagios) for p in no_caminho]):
        return False
    return not pontes[ponte]['os'] 

def pode_executar_transicao(transicao, pontes, estagios):
    estagio = estagios[transicao['origem']] if transicao['origem'] else estagios[transicao['destino']]
    if transicao['origem'] is None:
        return not estagio['os']

    if transicao['destino'] is None:
        return estagio['os'] == transicao['os'] and estagio['status'] == 'parado'

    no_caminho = pontes_no_caminho_considerando_movimento(transicao['ponte'], transicao['destino'], pontes)
    pode = all([ponte_pode_ser_movida_para_abrir_espaco(p, transicao['destino'], pontes, estagios) for p in no_caminho])
    pode = pode and not estagios[transicao['destino']]['os']
    pode = pode and estagios[transicao['origem']]['os'] == transicao['os']
    pode = pode and estagios[transicao['origem']]['status'] == 'parado'
    pode = pode and not (pontes[transicao['ponte']]['os'] or pontes[transicao['ponte']]['status'] == 'transportando')
    pode = pode and not estagios[transicao['destino']]['aguardando']
    pode = pode and pontes[transicao['ponte']]['estagio'][:2] == transicao['origem'][:2]
    return pode

def pode_executar_transicao_se_mover_ponte(transicao, pontes, estagios):
    estagio = estagios[transicao['origem']] if transicao['origem'] else estagios[transicao['destino']]
    if transicao['origem'] is None:
        return not estagio['os']

    if transicao['destino'] is None:
        return estagio['os'] == transicao['os'] and estagio['status'] == 'parado'

    no_caminho = pontes_no_caminho_considerando_movimento(transicao['ponte'], transicao['destino'], pontes)
    pode = all([ponte_pode_ser_movida_para_abrir_espaco(p, transicao['destino'], pontes, estagios) for p in no_caminho])
    pode = pode and not estagios[transicao['destino']]['os']
    pode = pode and estagios[transicao['origem']]['os'] == transicao['os']
    pode = pode and estagios[transicao['origem']]['status'] == 'parado'
    pode = pode and not (pontes[transicao['ponte']]['os'] or pontes[transicao['ponte']]['status'] == 'transportando')
    pode = pode and not estagios[transicao['destino']]['aguardando']
    #pode = pode and pontes[transicao['ponte']]['estagio'][:2] == transicao['origem'][:2]
    return pode

def executa_transicao(transicao, pontes, estagios, tempo_total=0):
    if transicao['destino'] is None and estagios[transicao['origem']]['os']:
        log('-> Executa transição de saída para O.S {}'.format(transicao['os'][0]), tempo_total)
        estagios[transicao['origem']]['os'] = None
        return transicao

    if transicao['origem'] is None and not estagios[transicao['destino']]['os']:
        log('-> Executa transição de entrada para O.S {} em {}'.format(transicao['os'], transicao['destino']), tempo_total)
        estagios[transicao['destino']]['os'] = transicao['os']
        estagios[transicao['destino']]['tempo_restante'] = tempo_execucao(transicao['destino'], transicao['os'][1])
        estagios[transicao['destino']]['status'] = 'processando'
        estagios[transicao['destino']]['aguardando'] = None
        return transicao

    if not pode_executar_transicao(transicao, pontes, estagios):
        raise RuntimeError(u'Transicao nao pode ser executada agora')
    for p in pontes_no_caminho_considerando_movimento(transicao['ponte'], transicao['destino'], pontes):
        move_ponte(p, pontes, pontes[p]['estagio'], transicao['destino'], os=None, estagios=estagios, tempo_total=tempo_total)

    move_ponte(transicao['ponte'], pontes, transicao['origem'], transicao['destino'], estagios[transicao['origem']]['os'], estagios, tempo_total)
    return transicao

# TOMAR MUITO CUIDADO COM [:2] NO ESTAGIO -- NÃO CONFIAR NO ESTÁGIO DA PONTE
# A ponte pode estar em CV02 e a transição é para CV01
def move_ponte(ponte, pontes, origem, destino, os, estagios, tempo_total):
    pontes[ponte]['status'] = 'transportando'
    pontes[ponte]['destino'] = destino
    if not os:
        pontes[ponte]['tempo_restante'] = tempo_deslocamento(origem, destino)/2
        log('>> Move ponte {ponte} para executar transicao'.format(ponte=ponte), tempo_total)
    else:
        pontes[ponte]['os'] = os
        pontes[ponte]['tempo_restante'] = tempo_deslocamento(pontes[ponte]['estagio'], destino)
        estagios[origem]['os'] = None
        estagios[destino]['aguardando'] = os
        kwargs = dict(origem=origem, destino=destino, os=os, ponte=ponte)
        log('î Executa transição de {origem} para {destino} com os {os} com ponte {ponte}'.format(**kwargs), tempo_total)

def log(msg, tempo_total):
    global DEBUG
    if DEBUG:
        print '['+str(tempo_total).rjust(5, '0')+'] '+msg

def libera_pontes(pontes, estagios, tempo_total):
    for p in pontes.keys():
        if pontes[p]['status'] == 'transportando' and pontes[p]['tempo_restante'] <= 0:
            if estagios[pontes[p]['destino']]['os'] and pontes[p]['os']:
                raise RuntimeError('Nao eh possivel liberar a ponte pois destino tem O.S')
            pontes[p]['status'] = 'parada'
            pontes[p]['estagio'] = pontes[p]['destino']
            os = pontes[p]['os']
            if os:
                estagio = pontes[p]['destino']
                assert estagios[estagio]['aguardando'] == os
                estagios[estagio]['os'] = os
                estagios[estagio]['aguardando'] = None
                estagios[estagio]['status'] = 'processando'
                estagios[estagio]['tempo_restante'] = tempo_execucao(pontes[p]['destino'], pontes[p]['os'][1])
                pontes[p]['destino'] = pontes[p]['os'] = None
                log('v Libera ponte {ponte} e adiciona os {os} em {estagio}'.format(ponte=p, os=os, estagio=estagio), tempo_total)
            else:
                pontes[p]['destino'] = None
                log('s Para {ponte} em {estagio}'.format(ponte=p, os=os, estagio=pontes[p]['estagio']), tempo_total)

def libera_estagios(estagios, tempo_total):
    for e in estagios.keys():
        if estagios[e]['tempo_restante'] <= 0 and estagios[e]['status'] == 'processando':
            os = estagios[e]['os']
            estagios[e]['status'] = 'parado'
            estagios[e]['tempo_restante'] = 0
            log('x Fim do processamento da os {os} no estagio {e}'.format(os=os, e=e), tempo_total)

def executa(pontes, estagios, transicoes):
    tempo_total = 0
    qtd_transicoes = len(transicoes)
    iteracoes_com_mesmo_numero_de_transicoes = 0
    transicoes_executadas = []
    while len(transicoes) > 0:
        remover = []
        if qtd_transicoes == len(transicoes):
            iteracoes_com_mesmo_numero_de_transicoes += 1
        else:
            iteracoes_com_mesmo_numero_de_transicoes = 0
            qtd_transicoes = len(transicoes)

        if iteracoes_com_mesmo_numero_de_transicoes > 10:
            print u'Parado há mais de {} iterações'.format(10)
            import pdb;pdb.set_trace()

        for t in transicoes:
            if pode_executar_transicao(t, pontes, estagios):
                executa_transicao(t, pontes, estagios, tempo_total)
                transicoes.remove(t)
                transicoes_executadas.append(t)
            elif pode_executar_transicao_se_mover_ponte(t, pontes, estagios):
                move_ponte(t['ponte'], pontes, pontes[t['ponte']]['estagio'], t['origem'], None, estagios, tempo_total)

        tempo_minimo_tick = min([estagios[e]['tempo_restante'] for e in estagios.keys() if estagios[e]['status']=='processando'] or [9999])
        tempo_minimo_pontes = [pontes[p]['tempo_restante'] for p in pontes.keys() if pontes[p]['status']=='transportando'] or [9999]
        tempo_minimo_tick = min(min(tempo_minimo_pontes), tempo_minimo_tick)
        if tempo_minimo_tick != 9999:
            tick(estagios, pontes, tempo_minimo_tick, tempo_total)
            tempo_total += tempo_minimo_tick
            libera_pontes(pontes, estagios, tempo_total)
            libera_estagios(estagios, tempo_total)
    return tempo_total

def dbg(v):
    print '\n'.join([unicode(vi) for vi in v])
