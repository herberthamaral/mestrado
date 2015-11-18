# encoding: utf-8

TEMPOS_DESLOCAMENTO = {
    'CV':{ 'RH': 10, 'FP': 15, 'LC': 15, 'CC': 10, 'BO': 10, },
    'RH':{ 'CV': 10, 'FP': 10, 'LC': 15, 'CC': 15, },
    'FP':{ 'CV': 15, 'RH': 10, 'LC': 15, 'CC': 10, },
    'LC':{ 'CV': 15, 'RH': 15, 'FP': 15, },
    'CC':{ 'BO': 6, 'CV': 10, 'FP': 10, 'RH': 15, },
    'BO':{ 'CV': 10, 'CC': 6},
}

TEMPOS_EXECUCAO = {
    'CV': 38, 'RH': '25', 'FP': 45, 'BO': 20, 
    'LC': {'A': 34, 'B': 34, 'C': 32},
    'CC':{'D': 75, 'E': 75, 'F': 70, 'G': 80, 'H': 65, 'I': 75, 'J': 70, 'K': 80, 'L': 30},
}

class Estagio(object):
    def __init__(self):
        self.status = 'pronto'
        self.tempo_restante = 0
        self.os = None

    def add_os(self, os):
        if self.status == 'pronto':
            self.status = 'trabalhando'
            self.os = os
            self.tempo_restante = self.tempo_total()
        else:
            raise RuntimeError(u'Estagio ocupado')

    def tick(self, tempo):
        if self.status == 'pronto':
            return
        self.tempo_restante -= tempo
        if self.tempo_restante <= 0:
            self.status = 'pronto'

    def obter_os_pronta(self):
        if self.status != 'pronto' or not self.os:
            raise RuntimeError(u'Nao existe O.S pronta')
        os = self.os
        self.os = None
        return os

    def tempo_total(self):
        raise RuntimeError('Implemente este metodo nas classes filhas')

    def sigla(self):
        raise RuntimeError('Implemente este metodo nas classes filhas')

class Convertedor(Estagio):
    def tempo_total(self):
        return 38

    def sigla(self):
        return 'CV'

class LingotamentoConvencional(Estagio):
    def tempo_total(self):
        return TEMPOS_EXECUCAO['LC'][self.os.aco]

    def sigla(self):
        return 'LC'

class LingotamentoContinuo(Estagio):
    def tempo_total(self):
        return TEMPOS_EXECUCAO['CC'][self.os.aco]

    def sigla(self):
        return 'CC'

class FornoPanela(Estagio):
    def tempo_total(self):
        return 45

    def sigla(self):
        return 'FP'

class DesgaiseficacaoVacuo(Estagio):
    def tempo_total(self):
        return 25

    def sigla(self):
        return 'RH'

class EstacaoBorbulhamento(Estagio):
    def tempo_total(self):
        return 20

    def sigla(self):
        return 'EB'

class OrdemServico(object):
    def __init__(self, aco=''):
        self.aco = aco
        self.estado = None

class Ponte(object):
    def __init__(self, localizacao):
        self.localizacao = localizacao

    def pega_os_do_estagio(self, estagio):
        self.localizacao = estagio
        self.estagio_origem = estagio
        self.os = estagio.obter_os_pronta()
        self.status = 'trabalhando'

    def entrega_os_no_estagio(self, estagio):
        self.estagio_destino = estagio
        self.tempo_restante = self.tempo_total()

    def tempo_total(self):
        return TEMPOS_DESLOCAMENTO[self.estagio_origem.sigla()][self.estagio_destino.sigla()]

    def tick(self, tempo):
        self.tempo_restante -= tempo
        if self.tempo_restante <= 0:
            self.status = 'parado'
            self.estagio_destino.add_os(self.os)
            self.localizacao = self.estagio_destino
            self.os = None

class Transicao(object):
    def __init__(self, os, origem, destino, ponte):
        self.os = os
        self.origem = origem
        self.destino = destino
        self.ponte = ponte
        self.estagios = dict()
        self.concluida = False
        self.pontes = []
        self.status = 'parado'
        self.tempo_restante = 0

    def add_estagio(self, nome, obj):
        if not self.estagios.get(nome):
            self.estagios[nome] = []
        self.estagios[nome].append(obj)

    def add_ponte(self, ponte):
        self.pontes.append(ponte)

    def tick(self, tempo):
        #refatorar urgente
        if self.tempo_restante == 0 and self.origem and self.destino:
            self.tempo_restante = TEMPOS_DESLOCAMENTO[self.origem][self.destino]
            self.ponte.pega_os_do_estagio(self.estagios[self.origem][0])
        if not self.origem:
            self.estagios[self.destino][0].add_os(self.os)
            self.concluida = True
        else:
            if self.status == 'parado':
                self.ponte.entrega_os_no_estagio(self.estagios[self.destino][0])
            self.status = 'trabalhando'
            self.tempo_restante -= tempo
            self.ponte.tick(tempo)

            if self.tempo_restante <= 0:
                self.concluida = True
                self.estado = 'parado'

class Aciaria(object):
    def __init__(self):
        self.convertedor1 = Convertedor()
        self.convertedor2 = Convertedor()
        self.desgaiseficacao = DesgaiseficacaoVacuo()
        self.forno_panela = FornoPanela()
        self.borbulhamento = EstacaoBorbulhamento()
        self.lingotamento_convencional = LingotamentoConvencional()
        self.lingotamento_continuo = LingotamentoContinuo()
        self.estagios = [self.convertedor1, self.convertedor2,
                         self.desgaiseficacao, self.forno_panela, self.borbulhamento,
                         self.lingotamento_convencional,
                         self.lingotamento_continuo]
        self.transicoes = []

    def add_transicao(self, origem, destino, os, ponte):
        self.transicoes.append(dict(origem=origem, destino=destino, os=os, ponte=ponte))
