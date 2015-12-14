# encoding: utf-8

def test_pontes_no_caminho_ponte_A_para_FP_deve_retornar_B():
    import pontes 
    assert pontes.pontes_no_caminho('A', 'FP', pontes.pontes) == ['B']

def test_pontes_no_caminho_ponte_A_para_CC_deve_retornar_B_e_C():
    import pontes 
    assert pontes.pontes_no_caminho('A', 'CC', pontes.pontes) == ['B', 'C']

def test_pontes_no_caminho_ponte_A_para_CV1_deve_retornar_nada():
    import pontes 
    assert pontes.pontes_no_caminho('A', 'CV1', pontes.pontes) == []

def test_pontes_no_caminho_ponte_B_para_FP_deve_retornar_nada():
    import pontes 
    assert pontes.pontes_no_caminho('B', 'FP', pontes.pontes) == []

def test_pontes_no_caminho_ponte_B_para_CV1_deve_retornar_A_quando_todos_estao_no_meio():
    import pontes 
    pontes.pontes['A']['estagio'] = 'FP'
    pontes.pontes['B']['estagio'] = 'FP'
    pontes.pontes['C']['estagio'] = 'FP'
    assert pontes.pontes_no_caminho('B', 'CV1', pontes.pontes) == ['A']

def test_pontes_no_caminho_ponte_C_para_FP_deve_retornar_A_B_quando_todos_estao_na_direita():
    import pontes 
    pontes.pontes['A']['estagio'] = 'CC'
    pontes.pontes['B']['estagio'] = 'CC'
    pontes.pontes['C']['estagio'] = 'CC'
    assert pontes.pontes_no_caminho('C', 'FP', pontes.pontes) == ['A', 'B']
