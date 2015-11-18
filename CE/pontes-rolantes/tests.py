# encoding: utf-8
from statemachine import (Convertedor, OrdemServico, LingotamentoConvencional,
                          LingotamentoContinuo, Ponte, FornoPanela, Aciaria, Transicao)

def test_convertedor_deve_contar_ticks():
    estagio = Convertedor()
    os = OrdemServico()
    estagio.add_os(os)
    estagio.tick(20)
    assert estagio.tempo_restante == 18

def test_convertedor_deve_marcar_tarefa_como_pronta_quando_tiver():
    estagio = Convertedor()
    os = OrdemServico()
    estagio.add_os(os)
    assert estagio.status == 'trabalhando'
    estagio.tick(38)
    assert estagio.status == 'pronto'

def test_convertedor_deve_reclamar_quando_mais_de_uma_os_for_colocada_ao_mesmo_tempo():
    estagio = Convertedor()
    os = OrdemServico()
    estagio.add_os(os)
    try:
        estagio.add_os(os)
        raise Exception(u'Não deve ser possível adicionar duas O.S')
    except RuntimeError:
        pass

def test_convertedor_nao_deve_contar_tempo_quando_nao_tiver_os():
    estagio = Convertedor()
    estagio.tick(10)
    assert estagio.tempo_restante == 0

def test_lingotamento_convencional_deve_apresentar_tempo_correto_dependendo_da_os():
    lco = LingotamentoConvencional()
    os = OrdemServico(aco='A')
    lco.add_os(os)
    assert lco.tempo_total() == 34

def test_lingotamento_continuo_deve_apresentar_tempo_correto_dependendo_da_os():
    lco = LingotamentoContinuo()
    os = OrdemServico(aco='D')
    lco.add_os(os)
    assert lco.tempo_total() == 75

def test_ponte_deve_poder_executar_trabalho():
    os = OrdemServico()
    convertedor = Convertedor()
    ponte = Ponte(convertedor)
    convertedor.add_os(os)
    convertedor.tick(38)
    forno_panela = FornoPanela()
    ponte.pega_os_do_estagio(convertedor)
    ponte.entrega_os_no_estagio(forno_panela)
    assert ponte.status == 'trabalhando'
    ponte.tick(15)
    assert ponte.status == 'parado'
    assert forno_panela.os == os

def test_estagio_deve_rejeitar_pedido_de_os_pronta_em_progresso():
    estagio = Convertedor()
    estagio.add_os(OrdemServico())
    try:
        estagio.obter_os_pronta()
        raise Exception(u'Não deve ser possível obter a O.S quando não está pronta')
    except RuntimeError:
        pass

def test_deve_ser_possivel_executar_transicoes():
    os = OrdemServico('A')
    transicao = Transicao(os=os, origem=None, destino='CV', ponte=None)
    cv = Convertedor()
    transicao.add_estagio('CV', cv)
    transicao.tick(15)
    assert transicao.concluida
    assert transicao.estagios['CV'][0].status == 'trabalhando'

def test_deve_ser_possivel_executar_transicoes_com_pontes():
    os = OrdemServico('A')
    transicao = Transicao(os=os, origem=None, destino='CV', ponte=None)
    cv = Convertedor()
    fp = FornoPanela()
    transicao.add_estagio('CV', cv)
    transicao.tick(15)
    pontea, ponteb, pontec = Ponte(cv), Ponte(cv), Ponte(fp)
    transicao = Transicao(os=os, origem='CV', destino='FP', ponte=pontea)
    transicao.add_estagio('CV', cv)
    transicao.add_estagio('FP', fp)
    cv.tick(38)
    transicao.add_ponte(pontea)
    transicao.add_ponte(ponteb)
    transicao.add_ponte(pontec)
    transicao.tick(15)
    assert transicao.concluida
    assert transicao.estagios['CV'][0].status == 'pronto'
    assert pontea.localizacao == fp
