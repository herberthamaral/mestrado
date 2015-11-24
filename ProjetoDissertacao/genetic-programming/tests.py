import sys
from gp import execute, gen_random_tree, replace_element_bfs, plain, get_element_by_pos

def test_funcao_vazia_retorna_none():
    ftree = []
    assert execute(ftree) == None

def test_funcao_somente_com_var_retorna_var():
    ftree = ['a']
    kwargs = {'a': 1}
    assert execute(ftree, kwargs) == 1

def test_escalar_simples():
    ftree = [1]
    assert execute(ftree) == 1

def test_funcao_sum():
    ftree = ['+', 1, 2]
    assert execute(ftree) == 3

def test_sum_profundidade_1():
    ftree = ['+', ['+', 2,3], 2]
    assert execute(ftree) == 7

def test_sum_profundidade_2():
    ftree = ['+', ['+', 2,3], ['-', 5, ['*', 2, 3]]]
    assert execute(ftree) == 4

def test_var():
    ftree = ['+', 'a', 2]
    kwargs = {'a': 3}
    assert execute(ftree, kwargs) == 5

def test_mult_sum():
    ftree = ['+', 1, 2, 3]
    assert execute(ftree) == 6

def test_gen_random_tree_pode_gerar_arvores_validas():
    tree = gen_random_tree(range(1,5))
    execute(tree)

def test_bfs():
    tree = ['+', ['-', 5, 6], ['*', ['+', 1, 2], 4]]
    replace_element_bfs(5, tree, ['-', 1, 1])
    expected_tree = ['+', ['-', 5, 6], ['*', ['-', 1, 1], 4]]
    assert tree == expected_tree

def test_plain():
    tree = ['+', ['-', 5, 6], ['*', ['+', 1, 2], 4]]
    assert plain(tree) == ['+', '-', 5, 6, '*', '+', 1, 2, 4]

def test_get_element_by_pos():
    tree = ['+', ['-', 5, 6], ['*', ['+', 1, 2], 4]]
    assert get_element_by_pos(tree, 5) == ['+', 1, 2]
