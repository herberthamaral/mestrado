2.1 a) 

Grupo 1: x1,x2,x3
Grupo 2: x1,x2,x3

2.1 b)

Centróide 1: [2.00, 1.33]
Centróide 2: [5.00, 2.66]

2.1 c) Testando com dois tipos de normalização (escore-z e minmax), nenhuma
técnica fez com que o algoritmo de agrupamento apresentasse resultados
diferentes. 

Foram feitos testes com apenas uma iteração e com três iterações, com dados
normalizados e não-normalizados, sempre com os mesmos resultados. Todos os
testes foram executados  utilizando C1 = [1,2] e C2 = [4,2] como centróides
iniciais.

No entanto, por causa de discrepâncias nas escalas dados reais, torna-se
necessário normalizar os dados antes dos agrupamentos. Especula-se que a
não-diferença notada no dataset deste exemplo deve-se ao fato dos dois tipos de
dados estarem na mesma escala.

2.1 d) Executando o algoritmo com dois critérios de parada (100 iterações e 0.5
para movimentação de centróide), em todos os casos o critério de parada de
movimentação de centróide foi o motivo de parada. Portanto pode-se dizer que o
algoritmo estabilizou.

2.1 e) Uma possível interpretação é a classe social do cliente. Clientes com
melhor condição financeira gasta mais com vestuário e tende a gastar pelo menos
a mesma quantia com alimentação.

2.2)

a)

x2--
    |-- 1.41
x1--   | ------- 1.42
x3-----         |
x4 ---          | - 3.20 
      | -- 1.00 |
x5 ---    | ---- 2.41
x6 -------

O intervalo de corte fica entre os grupos (x1, x2, x3) e (x4, x5, x6)
