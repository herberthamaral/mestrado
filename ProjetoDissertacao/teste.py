# encoding: utf-8
from jellyfish import jaro_winkler
import itertools

tuplas = (
    (u'João Pedro da Silva',u'01/04/1985',u'Rua das Camélias 325',u'92368080',),
    (u'João Pedro Silva',u'01/04/1985',u'Rua das Tulipas 180',u'92338080',),
    (u'Joana Paula Silva',u'02/09/1992',u'Rua das Tulipas 180',u'32225478',),
    (u'Joana P. Silva',u'02/09/1962',u'Av. das Bromélias 98',u'32225478',),
)

media = lambda x: sum(x)/float(len(x))

for par_tuplas in itertools.combinations(tuplas, 2):
    score = []
    for i,t in enumerate(par_tuplas[0]):
        score.append(jaro_winkler(par_tuplas[0][i], par_tuplas[1][i]))
    print tuplas.index(par_tuplas[0])+1, '&', tuplas.index(par_tuplas[1])+1, '&', ' & '.join([str(i) for i in score]), '&', sum(score)
