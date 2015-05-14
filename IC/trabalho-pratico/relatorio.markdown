Primeiro trabalho prático - Inteligência computacional
======================================================

O presente trabalho analisa o uso de redes neurais artificiais do tipo
perceptron de múltiplas camadas para fazer classificação de dados de comparação
de registros, a fim de categoriza-los como registros correspondentes ou
não-correspondentes, em um processo conhecido como record linkage.

A base de dados contém os resultados de comparação de dados demográficos
provenientes do registro epidemiológico de câncer do estado alemão de
Rhine-Westphalia [1].

Record linkage
--------------

Esta seção contém uma breve introdução do processo de record linkage e foi
inteiramente inspirada em um survey sobre o assunto [2].

Record linkage é o processo de identificar registros diferentes ou múltiplos
que correspondem a uma entidade real ou a um objeto. Segundo o processo
é conhecido como outros nomes, como merge-purge, data deduplication, instance
identification, coreference resolution, identity uncertainty e duplicate
detection.

O processo de record linkage é composto majoritariamente de 3 fases: preparação
de dados, comparação de campos e, finalmente, detecção de duplicidade.

A fase de preparação de dados conta com os passos de análise, transformação de
dados e normalização de dados. Esta fase tem como objetivo remover
heterogenidades dos dados com o fim de facilitar (ou mesmo permitir) a
comparação. Um exemplo seria um processo de record linkage para achar
duplicações em uma base de dados de pacientes: os acentos dos nomes seriam
removidos, todas as letras seriam colocadas em minúsculo e contrações, como
"Ma" seriam convertidos para "Maria".

A fase de comparação de campos tem o objetivo de medir o nível de semelhança
entre os campos de dois registros previamente preparados. Essa métrica é obtida
através de comparação feita com algoritmos específicos que levam em conta a
distância de edição (distância Levenshtein, distância Jaro-Winkler,
Smith-Waterman, dentre outras), de token (strings atômicas, WHIRL) e
semelhança fonética (soundex, NYSSIIS, ONCA, Metaphone).

Finalmente, há a fase de detecção de registros duplicados. Nesta fase, os dados
provenientes da etapa anterior são analisados e classificados entre
correspondentes ou não-correspondentes. Esta classifcação pode ser
probabilística ou determinística.
 
Características da base de dados
--------------------------------

A base de dados é composta de registros provenientes da fase de comparação de
dados e cada linha contém as seguintes informações:

1. id_1: identificador do primeiro registro.
2. id_2: identificador do segundo registro.
3. cmp_fname_c1: nível de concordância do primeiro nome, primeiro componente
4. cmp_fname_c2: nível de concordância do primeiro nome, segundo componente
5. cmp_lname_c1: nível de concordância do primeiro sobrnome, primeiro componente
6. cmp_lname_c2: nível de concordância do primeiro sobrnome, segundo componente
7. cmp_sex: nível de concordância do sexo
8. cmp_bd: nível de concordância agreement da data de nascimento, componente do dia
9. cmp_bm: nível de concordância agreement da data de nascimento, componente do mês
10. cmp_by: nível de concordância agreement da data de nascimento, componente do ano
11. cmp_plz: nível de concordância de código postal
12. is_match: indica se os dois registros são iguais (TRUE para iguais, FALSE para não-iguais)

Os níveis de concordância ficam entre 0 e 1, sendo que 0 indica nenhuma
semelhança/concordância e 1 indica total semelhança/concordância. No entanto, a
base de dados contém várias colunas contendo "?" (desconhecido). Estas colunas
foram substituídas por -1 para possibilitar o uso na rede neural.

Metodologia
-----------

A base de dados contém 5749132 registros, divididos em dez blocos de igual
tamanho. O primeiro bloco foi usado para treinar a rede neural e os outros
nove foram usados para validar o treinamento.

Os campos cmp_fname_c1, cmp_fname_c2, cmp_lname_c1, cmp_lname_c2, cmp_sex,
cmp_bd, cmp_bm, cmp_by e cmp_plz são usados como entrada da rede, que deverá
classificar o registro em correspondente ou não-correspondente. O campo
is_match é usado como saída esperada.

Para este trabalho, uma rede neural de duas camadas, contendo 16 neurônios na
camada intermediária foi usada. O toolbox de redes neurais do MatLab foi
utilizado.

O código-fonte utilizado para a realização deste trabalho pode ser encontrado
em https://github.com/herberthamaral/mestrado/tree/master/IC/trabalho-pratico
(acesso em 14/05/2015).

Resultados
----------

Os testes demonstraram um excelente resultado, em que apenas 108 registros num
5174210 foram classificados incorretamente, deixando a taxa de acerto da rede
em 99.9979%.

[1] - Irene Schmidtmann, Gael Hammer, Murat Sariyar, Aslihan Gerhold-Ay;
Evaluation des Krebsregisters NRW Schwerpunkt Record Linkage. Technical Report,
IMBEI 2009. Disponível em
https://archive.ics.uci.edu/ml/datasets/Record+Linkage+Comparison+Patterns,
acessado em 14/05/2015
[2] - Ahmed K. Elmagarmid, Panagiotis G. Ipeirotis, Vassilios S. Verykios;
Duplicate Record Detection: A Survey. IEEE TRANSACTIONS ON KNOWLEDGE AND DATA
ENGINEERING, VOL. 19, NO. 1, Janeiro de 2007.
