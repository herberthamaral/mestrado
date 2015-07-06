import numpy as np
import matplotlib.pyplot as plt

def f(t):
    return np.exp(-t) * np.cos(2*np.pi*t)

def _4n2(n):
    return np.power(np.multiply(4,n), 2)

def log(n):
    return np.log(n)/np.log(3)

def log2(n):
    return np.log(n)/np.log(2)

def _3n(n):
    return np.power(3, n)

def _20n(n):
    return np.multiply(n, 20)

def _n23(n):
    return np.power(n, 2/3.0)

t1 = np.arange(0.0, 3.0, 0.1)

plt.figure(1)
#plt.subplot(211)
plt.plot(t1, f(t1), 'k',
         t1, _4n2(t1),'r',
         t1, log(t1),'g',
         t1, _3n(t1),'b',
         t1, _20n(t1),'c',
         t1, log2(t1),'m',
         t1, _n23(t1),'y',
         )

plt.savefig('plot.png')
