# encoding: utf-8

#NOTA: scipy versão 0.14.0 utilizada
import time
from math import cos, sin,pi
from numpy.random import rand
from scipy.optimize import anneal

def gi(xi):
    return sin(2*pi*xi) + 0.5 <= 0

def hj(xj):
    return cos(2*pi*xj) + 0.5 == 0

def rastrigin(x, n):
    valor = 10*n + sum([x[i]**2 - 10*cos(2*pi*x[i]) for i in range(n)])
    return valor

def teste5min(n):
    initial = time.time()
    resp = dict(T0=1e5, Tf=10, x0=rand(1,n)[0])
    while initial + 1*60 > time.time():
        tf = float('1'+'0'*resp['Tf'])
        r = anneal(rastrigin, resp['x0'], (n,), maxiter=float('inf'), maxeval=float('inf'), maxaccept=float('inf'), feps=float('-inf'), lower=-5.12, upper=5.12, T0=1e5, Tf=tf, learn_rate=0.995, full_output=True,disp=False)
        resp['T0'] = r[2]
        resp['Tf'] += 2
        resp['x0'] = r[0]
    return r


if __name__=='__main__':
    print teste5min(3)
    #print 'n=3:', anneal(rastrigin, rand(1,3)[0], (3,), maxiter=10000, maxeval=10000, maxaccept=10000, feps=float('-inf'), lower=-5.12, upper=5.12, T0=1e5, Tf=1e-10, learn_rate=0.995, full_output=True,disp=False)
    #print 'n=5:', anneal(rastrigin, rand(1,5)[0], (5,), maxiter=10000, maxeval=10000, maxaccept=10000, feps=float('-inf'), lower=-5.12, upper=5.12, T0=1e5, Tf=1e-10, learn_rate=0.995, full_output=True,disp=False)
    #print 'n=10:', anneal(rastrigin, rand(1,10)[0], (10,), maxiter=10000, maxeval=10000, maxaccept=10000, feps=float('-inf'), lower=-5.12, upper=5.12, T0=1e5, Tf=1e-10, learn_rate=0.995, full_output=True,disp=False)
