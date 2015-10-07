# encoding: utf-8

#NOTA: scipy versão 0.14.0 utilizada
import time
from math import cos, sin,pi
from numpy.random import rand
from anneal import anneal

# metropolis = boltzmann

inf = float('inf')

def gi(xi):
    return sin(2*pi*xi) + 0.5 <= 0

def hj(xj):
    return cos(2*pi*xj) + 0.5 == 0

def rastrigin(x, n):
    if float('inf') in x or float('-inf') in x:
        return 1e5 #retorna um valor alto para penalizar
    valor = 10*n + sum([x[i]**2 - 10*cos(2*pi*x[i]) for i in range(n)])
    return valor

def teste5min(n):
    x0 = rand(1,n)[0]
    r = anneal(rastrigin, x0, (n,),
            maxiter=inf,
            maxeval=inf,
            maxaccept=inf,
            feps=-inf,
            lower=-5.12,
            upper=5.12,
            T0=1e5,
            Tf=1e-10,
            learn_rate=0.995,
            full_output=True,
            disp=False,
            max_execution_time=1*60,
            #ignore_feps=True,
            schedule='boltzmann',
            )
    return r


if __name__=='__main__':
    print teste5min(3)
    print teste5min(3)
    print teste5min(3)
    print teste5min(3)
    print teste5min(3)
    print 'n=3:', anneal(rastrigin, rand(1,3)[0], (3,), maxiter=1e4, maxeval=1e4, maxaccept=1e4, feps=-inf, lower=-5.12, upper=5.12, T0=1e5, Tf=1e-10, learn_rate=0.995, full_output=True,disp=False, schedule='boltzmann')
    #print 'n=5:', anneal(rastrigin, rand(1,5)[0], (5,), maxiter=10000, maxeval=10000, maxaccept=10000, feps=float('-inf'), lower=-5.12, upper=5.12, T0=1e5, Tf=1e-10, learn_rate=0.995, full_output=True,disp=False)
    #print 'n=10:', anneal(rastrigin, rand(1,10)[0], (10,), maxiter=10000, maxeval=10000, maxaccept=10000, feps=float('-inf'), lower=-5.12, upper=5.12, T0=1e5, Tf=1e-10, learn_rate=0.995, full_output=True,disp=False)
