Primeiro trabalho prático - Inteligência computacional
======================================================

O presente trabalho analisa o uso de redes neurais artificiais do tipo
perceptron de múltiplas camadas para fazer classificação de uma base de dados
proveniente da análise de registros duplicados do registro epidemiológico de
câncer do estado alemão de Rhine-Westphalia [1].

Cada linha da base de dados contém os seguintes dados:

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

As informações de igualdade de registros são provenientes de avaliação manual.

Metodologia
-----------

A base de dados contém 5749132 registros, divididos em dez blocos de igual
tamanho. O primeiro bloco foi usado para treinar a rede neural e os outros
nove foram usados para validar o treinamento.

Os campos cmp_fname_c1, cmp_fname_c2, cmp_lname_c1, cmp_lname_c2, cmp_sex,
cmp_bd, cmp_bm, cmp_by e cmp_plz são usados como entrada da rede, que deverá
classificar o registro em igual ou não-igual. O campo is_match é usado como
saída esperada.

Para este trabalho, uma rede neural de duas camadas, contendo 16 neurônios na
camada intermediária foi usada. Para efeitos de comodidade, o toolbox de redes
neurais do MatLab foi utilizado.

Resultados
----------

Os testes demonstraram um excelente resultado, em que apenas 108 registros num
5174210 foram classificados incorretamente, deixando a taxa de acerto da rede
em 99.9979%.

[1] - https://archive.ics.uci.edu/ml/datasets/Record+Linkage+Comparison+Patterns
