# encoding: utf-8

def test_pontes_no_caminho_ponte_A_para_FP_deve_retornar_B():
    import pontes
    pontes = reload(pontes)
    assert pontes.pontes_no_caminho('A', 'FP', pontes.pontes) == ['B']

def test_pontes_no_caminho_ponte_A_para_CC_deve_retornar_B_e_C():
    import pontes
    pontes = reload(pontes)
    assert pontes.pontes_no_caminho('A', 'CC', pontes.pontes) == ['B', 'C']

def test_pontes_no_caminho_ponte_A_para_CV1_deve_retornar_nada():
    import pontes
    pontes = reload(pontes)
    assert pontes.pontes_no_caminho('A', 'CV1', pontes.pontes) == []

def test_pontes_no_caminho_ponte_B_para_FP_deve_retornar_nada():
    import pontes
    pontes = reload(pontes)

    assert pontes.pontes_no_caminho('B', 'FP', pontes.pontes) == []

def test_pontes_no_caminho_ponte_B_para_CV1_deve_retornar_A_quando_todos_estao_no_meio():
    import pontes
    pontes = reload(pontes)

    pontes.pontes['A']['estagio'] = 'FPA01'
    pontes.pontes['B']['estagio'] = 'FPA01'
    pontes.pontes['C']['estagio'] = 'FPA01'
    assert pontes.pontes_no_caminho('B', 'CV1', pontes.pontes) == ['A']

def test_pontes_no_caminho_ponte_C_para_FP_deve_retornar_A_B_quando_todos_estao_na_direita():
    import pontes
    pontes = reload(pontes)

    pontes.pontes['A']['estagio'] = 'CC01'
    pontes.pontes['B']['estagio'] = 'CC01'
    pontes.pontes['C']['estagio'] = 'CC01'
    assert pontes.pontes_no_caminho('C', 'FP', pontes.pontes) == ['A', 'B']

def test_rota_colisao_A_em_CV01_para_FP_e_B_em_FP_para_CV01_1():
    import pontes
    pontes = reload(pontes)

    pontes.pontes['A']['estagio'] = 'CV01'
    pontes.pontes['A']['destino'] = 'FPA01'
    pontes.pontes['A']['status'] = 'transportando'

    pontes.pontes['B']['estagio'] = 'FPA01'
    pontes.pontes['C']['estagio'] = 'CC01'
    assert pontes.rota_colisao(ponte='B', destino='CV01', pontes=pontes.pontes)

def test_rota_colisao_A_em_CV01_para_FP_e_B_em_FP_para_CV01_2():
    import pontes
    pontes = reload(pontes)

    pontes.pontes['B']['estagio'] = 'FPA01'
    pontes.pontes['B']['destino'] = 'CV01'
    pontes.pontes['B']['status'] = 'transportando'

    pontes.pontes['A']['estagio'] = 'CV01'
    pontes.pontes['C']['estagio'] = 'CC01'
    assert pontes.rota_colisao(ponte='A', destino='FPA01', pontes=pontes.pontes)

def test_rota_colisao_A_em_CV01_para_FP_e_B_em_CV02_para_FP():
    import pontes
    pontes = reload(pontes)

    pontes.pontes['B']['estagio'] = 'CV01'
    pontes.pontes['B']['destino'] = 'FPA01'
    pontes.pontes['B']['status'] = 'transportando'

    pontes.pontes['A']['estagio'] = 'CV01'
    pontes.pontes['C']['estagio'] = 'CC01'
    assert not pontes.rota_colisao(ponte='A', destino='FPA01', pontes=pontes.pontes)

def test_pode_executar_transicao_retorna_true_se_ponte_vazia_destino_vazio_sem_pontes_no_caminho_os_pronta_na_origem():
    import pontes
    pontes = reload(pontes)

    pontes.estagios['CV01']['os'] = (1, 'A')
    pontes.estagios['CV01']['status'] = 'parado'
    pontes.pontes['B']['estagio'] = 'CV01'
    pontes.pontes['B']['os'] = None
    pontes.pontes['B']['status'] = 'parada'
    pontes.pontes['A']['estagio'] = 'CV01'
    pontes.pontes['C']['estagio'] = 'FPA01'
    transicao = {'origem': 'CV01',  'destino': 'FPA01', 'os': (1, 'A'), 'ponte': 'B'}
    assert pontes.pode_executar_transicao(transicao, pontes.pontes, pontes.estagios)

def test_pode_executar_transicao_retorna_false_se_ponte_vazia_destino_vazio_sem_pontes_no_caminho_os_pronta_na_origem_ponte_fora_da_origem():
    import pontes
    pontes = reload(pontes)

    pontes.estagios['CV01']['os'] = (1, 'A')
    pontes.estagios['CV01']['status'] = 'parado'
    pontes.pontes['B']['estagio'] = 'RH01'
    pontes.pontes['B']['os'] = None
    pontes.pontes['B']['status'] = 'parada'
    pontes.pontes['A']['estagio'] = 'CV01'
    pontes.pontes['C']['estagio'] = 'FPA01'
    transicao = {'origem': 'CV01',  'destino': 'FPA01', 'os': (1, 'A'), 'ponte': 'B'}
    assert not pontes.pode_executar_transicao(transicao, pontes.pontes, pontes.estagios)

def test_pode_executar_transicao_se_mover_ponte_retorna_true_se_ponte_vazia_destino_vazio_sem_pontes_no_caminho_os_pronta_na_origem_ponte_fora_da_origem():
    import pontes
    pontes = reload(pontes)

    pontes.estagios['CV01']['os'] = (1, 'A')
    pontes.estagios['CV01']['status'] = 'parado'
    pontes.pontes['B']['estagio'] = 'RH01'
    pontes.pontes['B']['os'] = None
    pontes.pontes['B']['status'] = 'parada'
    pontes.pontes['A']['estagio'] = 'CV01'
    pontes.pontes['C']['estagio'] = 'FPA01'
    transicao = {'origem': 'CV01',  'destino': 'FPA01', 'os': (1, 'A'), 'ponte': 'B'}
    assert pontes.pode_executar_transicao_se_mover_ponte(transicao, pontes.pontes, pontes.estagios)


def test_pode_executar_transicao_retorna_false_se_ponte_ocupada_destino_vazio_sem_pontes_no_caminho_os_pronta_na_origem():
    import pontes
    pontes = reload(pontes)

    pontes.estagios['CV01']['os'] = (1, 'A')
    pontes.estagios['CV01']['status'] = 'pronto'
    pontes.pontes['B']['estagio'] = 'CV01'
    pontes.pontes['B']['os'] = (2, 'A')
    pontes.pontes['B']['status'] = 'transportando'

    pontes.pontes['A']['estagio'] = 'CV01'
    pontes.pontes['C']['estagio'] = 'FPA01'
    transicao = {'origem': 'CV01',  'destino': 'FPA01', 'os': (1, 'A'), 'ponte': 'B'}
    assert not pontes.pode_executar_transicao(transicao, pontes.pontes, pontes.estagios)

def test_pode_executar_transicao_retorna_false_se_ponte_vazia_destino_ocupado_sem_pontes_no_caminho_os_pronta_na_origem():
    import pontes
    pontes = reload(pontes)
    pontes.estagios['CV01']['os'] = (1, 'A')
    pontes.estagios['CV01']['status'] = 'pronto'
    pontes.estagios['FPA01']['os'] = (3, 'A')
    pontes.estagios['FPA01']['status'] = 'pronto'

    pontes.pontes['B']['estagio'] = 'CV01'
    pontes.pontes['B']['os'] = None
    pontes.pontes['B']['status'] = 'parada'

    pontes.pontes['A']['estagio'] = 'CV01'
    pontes.pontes['C']['estagio'] = 'FPA01'
    transicao = {'origem': 'CV01',  'destino': 'FPA01', 'os': (1, 'A'), 'ponte': 'B'}
    assert not pontes.pode_executar_transicao(transicao, pontes.pontes, pontes.estagios)

def test_pode_executar_transicao_retorna_true_se_ponte_vazia_destino_vazio_com_pontes_no_caminho_movendo_para_destino_os_pronta_na_origem():
    import pontes
    pontes = reload(pontes)
    pontes.estagios['CV01']['os'] = (1, 'A')
    pontes.estagios['CV01']['status'] = 'parado'

    pontes.pontes['B']['estagio'] = 'CV01'
    pontes.pontes['B']['os'] = None
    pontes.pontes['B']['status'] = 'transportando'
    pontes.pontes['B']['destino'] = 'FPA01'

    pontes.pontes['A']['estagio'] = 'CV01'
    pontes.pontes['C']['estagio'] = 'FPA01'
    transicao = {'origem': 'CV01',  'destino': 'FPA01', 'os': (1, 'A'), 'ponte': 'A'}
    assert pontes.pode_executar_transicao(transicao, pontes.pontes, pontes.estagios)


def test_pode_executar_transicao_retorna_false_se_ponte_aguardando_os_destino_vazio_com_pontes_no_caminho_movendo_para_destino_os_pronta_na_origem():
    import pontes
    pontes = reload(pontes)
    pontes.estagios['CV01']['os'] = (1, 'A')
    pontes.estagios['CV01']['status'] = 'parado'

    pontes.pontes['B']['estagio'] = 'CV01'
    pontes.pontes['B']['os'] = None
    pontes.pontes['B']['status'] = 'transportando'
    pontes.pontes['B']['destino'] = 'FPA01'

    pontes.estagios['FPA01']['aguardando'] = (2, 'A') # aguardando outra O.S

    pontes.pontes['A']['estagio'] = 'CV01'
    pontes.pontes['C']['estagio'] = 'FPA01'
    transicao = {'origem': 'CV01',  'destino': 'FPA01', 'os': (1, 'A'), 'ponte': 'A'}
    assert not pontes.pode_executar_transicao(transicao, pontes.pontes, pontes.estagios)

def test_pode_executar_transicao_retorna_true_se_origem_None_e_CV_desocupado():
    import pontes
    pontes = reload(pontes)

    transicao = {'origem': None,  'destino': 'CV01', 'os': (1, 'A'), 'ponte': 'A'}
    assert pontes.pode_executar_transicao(transicao, pontes.pontes, pontes.estagios)

def test_pode_executar_transicao_retorna_true_se_origem_cc01_e_destino_None():
    import pontes
    pontes = reload(pontes)

    transicao = {'origem': 'CC01',  'destino': None, 'os': (1, 'A'), 'ponte': 'A'}
    pontes.estagios['CC01']['os'] = (1, 'A')
    assert pontes.pode_executar_transicao(transicao, pontes.pontes, pontes.estagios)

def test_ponte_pode_ser_movida_para_abrir_espaco_1():
    import pontes
    pontes = reload(pontes)
    assert pontes.ponte_pode_ser_movida_para_abrir_espaco('B', 'FPA01', pontes.pontes, pontes.estagios)

def test_ponte_pode_ser_movida_para_abrir_espaco_2():
    import pontes
    pontes = reload(pontes)
    pontes.pontes['A']['estagio'] = 'CC01'
    pontes.pontes['B']['estagio'] = 'CC01'
    pontes.pontes['C']['estagio'] = 'CC01'
    assert pontes.ponte_pode_ser_movida_para_abrir_espaco('B', 'FPA01', pontes.pontes, pontes.estagios)

def test_ponte_pode_ser_movida_para_abrir_espaco_3():
    import pontes
    pontes = reload(pontes)
    pontes.pontes['A']['estagio'] = 'CC01'
    pontes.pontes['A']['os'] = (1, 'A')

    pontes.pontes['B']['estagio'] = 'CC01'
    pontes.pontes['C']['estagio'] = 'CC01'
    assert not pontes.ponte_pode_ser_movida_para_abrir_espaco('B', 'FPA01', pontes.pontes, pontes.estagios)

def test_executa_transicao_deve_colocar_pontes_em_moviemento_remover_os_da_fonte_e_fazer_ponte_destino_esperar():
    import pontes
    pontes = reload(pontes)
    transicao = {'origem': 'CV01',  'destino': 'FPA01', 'os': (1, 'A'), 'ponte': 'A'}
    pontes.estagios['CV01']['os'] = (1, 'A')
    pontes.estagios['CV01']['status'] = 'parado'
    pontes.executa_transicao(transicao, pontes.pontes, pontes.estagios)
    assert pontes.estagios['CV01']['os'] is None
    assert pontes.estagios['FPA01']['aguardando'] == (1, 'A')
    assert pontes.pontes['A']['os'] == (1, 'A')
    assert pontes.pontes['A']['status'] == 'transportando'
    assert pontes.pontes['B']['status'] == 'transportando'
    assert pontes.pontes['B']['os'] is None
    assert pontes.pontes['B']['destino'] == 'FPA01'

def test_executa_transicao_deve_conseguir_executar_transicoes_de_saida():
    import pontes
    pontes = reload(pontes)

    transicao = {'origem': 'CC01',  'destino':None, 'os': (1, 'A'), 'ponte': 'A'}
    pontes.estagios['CC01']['os'] = (1, 'A')
    pontes.executa_transicao(transicao, pontes.pontes, pontes.estagios)
    assert pontes.estagios['CC01']['os'] is None

def test_executa_transicao_deve_conseguir_executar_transicoes_de_entrada():
    import pontes
    pontes = reload(pontes)

    transicao = {'origem': None,  'destino': 'CV01', 'os': (1, 'A'), 'ponte': 'A'}
    pontes.executa_transicao(transicao, pontes.pontes, pontes.estagios)
    assert pontes.estagios['CV01']['os'] == (1, 'A')

def test_libera_pontes_up_deve_liberar_pontes_com_carga():
    import pontes
    pontes = reload(pontes)

    pontes.pontes['A']['estagio'] = 'CV01'
    pontes.pontes['A']['os'] = (1, 'A')
    pontes.pontes['A']['destino'] = 'FPA01'
    pontes.pontes['A']['status'] = 'transportando'
    pontes.pontes['A']['tempo_restante'] = 0
    pontes.pontes['B']['estagio'] = 'FPA01'
    pontes.estagios['FPA01']['aguardando'] = (1, 'A')
    pontes.libera_pontes(pontes.pontes, pontes.estagios, 0)
    assert pontes.pontes['A']['estagio'] == 'FPA01'
    assert pontes.pontes['A']['os'] is None
    assert pontes.pontes['A']['destino'] is None
    assert pontes.pontes['A']['status'] == 'parada'
    assert pontes.estagios['FPA01']['status'] == 'processando'
    assert pontes.estagios['FPA01']['tempo_restante'] == 45
    assert pontes.estagios['FPA01']['os'] == (1, 'A')
    assert pontes.estagios['FPA01']['aguardando'] == None
