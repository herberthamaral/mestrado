Universidade Estadual de Montes Claros - UNIMONTES
Centro de Ciências Exatas e Tecnológicas - CCET
Programa de Pós-Graduação em Modelagem Computacional e Sistemas - PPGMCS
Disciplina de Inteligência Computacional





Dissertação sobre redes neurais artificiais.
============================================


Redes neurais representam um conjunto de tecnologias que possuem fundamentos em
diversas áreas como neurociências, matemática, estatística, física, ciência da
computação e engenharia e que possuem uma propriedade especial: a de "aprender"
a partir de dados de entrada, com ou sem um "professor" [HAKIN, 1999].

Esta dissertação sobre o tema visa fazer um apanhado geral de conceitos-chave
do assunto.

Funcionamento do neurônio artificial
------------------------------------

A peça-chave das redes neurais artificiais é o neurônio artificial. Este
neurônio artificial é baseado numa simplificação do neurônio biológico e que
conta com basicamente quatro componentes: os pesos sinápticos, opcionalmente um
viés (bias), uma função soma e uma função de ativação.

No neurônio biológico, a excitação das sinapses pode fazer disparar um pulso
elétrico para outros neurônios. No neurônio artificial, esssa excitação é dada
pela entrada da rede e o disparo ou não disparo é feito pela função de ativação
do neurônio.

Matematicamente falando um neurônio é definido como

y = phi(sum(WjXj))

Em que:

- Wj é o peso sináptico da entrada j
- Xj é a entrada j
- phi é a função de ativação
- y é a saída do neurônio, que indica o disparo ou não-disparo do neurônio

Este tipo de neurônio é conhecido como neurônio de McCulloch-Pitts,
desenvolvido em 1943.

Assim como no neurônio biológico, o neurônio artificial precisa disparar
dependendo da entrada. Fazendo uma analogia com um aprendizado humano, quando
ensinamos conceitos binários para uma criança, como por exemplo dia e noite,
quente e frio, biologicamente falando estamos ensinando aos neurônios da
criança quando eles precisam e não-precisam disparar. Esta analogia
aplica-se a este modelo de neurônio de forma que ensinamos o neurônio a
disparar nas condições corretas. Este "aprendizado" é feito com o ajuste dos
pesos sinápticos que serão detalhados mais adiante.

Antes do assunto aprendizado ser tratado, é necessário detalhar os tipos e
objetivos das funções de ativação.

Objetivos principais da função de ativação
------------------------------------------

O objetivo principal de uma função de ativação é limitar a amplitude da saída
do neurônio [HAKIN, 1999]. Isso basicamente significa que, independente da
entrada, a função de ativação sempre funcionará em um intervalo (geralmente
entre 0 e 1), discreto ou contínuo, definido.

Basicamente temos três tipos de função de ativação: limiar, piecewise-linear, e
sigmoidal.

A função limiar (threshold) tem a seguinte forma geral:

phi(v) = {
            1 se v >=0
            0 se v < 0
         }
Em que v representa a saída da função somatório. Segue abaixo a representação
gráfica da função limiar:

(colocar representação gráfica)

A piecewise-linear possui uma forma que lembra a função limiar:

phi(v) = {
            1 se v>= 1/2
            v se 1/2 > v > -1/2
            0 se v<= -1/2
          }

É interessante observar que para valores absolutos grandes (>1/2) de v, a função
piecewise funciona como a função limiar. Segue abaixo a representação gráfica
da função limiar:

(colocar representação gráfica)

A função sigmoidal possui um gráfico com o formato de um "S" e é a função de
ativação mais comum em redes neurais artificiais [HAYKYN, 1999]. Esta função é
um balanceamento entre um comportamento linear e não-linear:

phi(v) = 1/(1+exp(-av))

Em que "a" é o parâmetro de "declive" da função, em que maiores valores de "a"
significarão uma diminuição da suavização da curva, como mostrado no gráfico abaixo:

(colocar representação gráfica)

Tipos de aprendizado
--------------------

A principal propriedade de uma rede neural é a habilidade de aprender.
Genericamente falando, o aprendizado consiste em atualização dos pesos
sinápticos para que a rede neural ative corretamente dado uma entrada.

Os tipos de aprendizado podem ser classificados em duas grandes categorias:
aprendizado supervisionado e não-supervisionado.

No aprendizado supervisionado, a rede neural terá um "professor" para dar a
resposta correta dado uma entrada. A partir da resposta do professor, a rede
neural utilizará mecanismos de correção de pesos para, caso a resposta esteja
errada, corrigir os pesos sinápticos. Utilizando novamente da analogia de
aprendizado humano, o aprendizado supervisionado acontece em situações quando
alguém pergunta algo para uma pessoa e corrige esta pessoa caso esteja errada.
Alguns exemplos de redes neurais que utilizam aprendizado supervisionado são:
neurônio de McCulloch-Pitts, Perceptron de Múltiplas Camadas, máquinas de
boltzmann restritas.

O aprendizado não-supervisionado não conta com um professor. Neste caso, a rede
neural tenta encontrar uma estrutura em dados não-rotulados. Na analogia com o
aprendizado humano um aprendizado não-supervisionado seria parecido a pedir uma
pessoa para separar objetos de diferentes tipos, como separar maçãs de
laranjas.

Tipos de redes neurais e seus algoritmos de aprendizado
-------------------------------------------------------

O perceptron é o tipo mais básico de rede neural, possui aprendizado
supervisionado, e serve como um classificador linear. Isso significa
que o perceptron consegue aprender a classificar dois tipos de dados rotulados.

A função de treinamento mais simples do perceptron consiste ajustar o peso
sináptico baseando-se na diferença entre o resultado esperado e o produzido
pela rede multiplicado por uma taxa de aprendizado alfa (geralmente < 1):

w = w + alfa(saída desejada - saída produzida)x

A rede neural Perceptron de Múltiplas Camadas (PMC ou MLP, na sigla em inglês)
consiste em uma combinação de camadas de perceptrons (geralmente 2 ou 3) e
possui um poder maior de classificação do que um único perceptron. Seu
algoritmo de aprendizado é o backpropagation, que consiste basicamente em
propagar o erro para camadas anteriores à camada de saída para que seja
possível atualizar os respectivos pesos dos neurônios.

A rede de Kohonen é um tipo de rede neural que utiliza aprendizado
não-supervisionado para fazer classificação de um número limitado (geralmente
dois) de categorias. Os neurônios da rede de Kohonen são representações de
vetores num plano cartesiano em que o objetivo do treinamento é aproximar os
vetores de agrupamentos de outros vetores, de forma que o neurônio fique o mais
equidistante possível da média dos vetores que ele classifica.

Aplicações de redes neurais
---------------------------

No decorrer do texto encontra-se algumas aplicações das redes neurais. Esta
seção provê uma maior especificação das aplicações de redes neurais.

Dentre as principais aplicações de redes neurais, encontram-se:

- Aproximação de funções onde um modelo matemático preciso é difícil de ser
desenvolvido.
- Classificação, que inclui reconhecimento de padrões, reconhecimento de
  sequências, e tomada de decisão. Dentre aplicações específicas deste tipo de
  uso encontram-se: reconhecimento de voz, face e dígitos, detecção de falhas e
  detecção de fraudes.
- Processamento de dados, incluindo filtragem, clusterização e compressão.

Considerações finais
--------------------

Este texto apenas arranha levemente a superfície do assunto redes neurais
artificiais. Há uma infinidade de outros assuntos não tratados que são
igualmente importantes e interessantes, como redes neurais profundas (deep
believe neural networks), que recentemente ganhou destaque por conseguir um
grau elevado de qualidade em deteção e classificação de padrões;
