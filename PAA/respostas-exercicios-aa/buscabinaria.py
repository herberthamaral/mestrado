def busca_binaria(vetor, n):
    fim = len(vetor)
    inicio = 0
    pivo = fim/2
    num_ops = 1
    while pivo != inicio and pivo != fim:
        if vetor[pivo] == n:
            return (pivo, num_ops, len(vetor))
        if vetor[pivo] < n:
            inicio = pivo
        else:
            fim = pivo
        pivo = (inicio + fim)/2
        num_ops += 1
    return -1

print busca_binaria(xrange(10), 2)
print busca_binaria(xrange(100), 2)
print busca_binaria(xrange(1000), 2)
print busca_binaria(xrange(10000), 2)
print busca_binaria(xrange(100000), 2)
print busca_binaria(xrange(1000000L), 2)
print busca_binaria(xrange(10000000L), 2)
print busca_binaria(xrange(100000000L), 2)
