Segunda aula prática
====================

Instruções:
-----------

- Implementar kmeans e kmeans++
- Estrutura de dados: matrizes e arrays do numpy
- Base Ruspini + 3 bases do repositório (bases numéricas de dimensões > 2).
- Executar 30 vezes nas mesmas condições iniciais e mesmo critério de parada
- Cálculo de performance: cálculo de quartis (box plot - ver matplotlib)
- Teste de NORMALIDADE: verificar se a base de dados foi amostrada com uma distribuição normal.
- Usar Wilcoxon signed rank para comparar os algoritmos (ver numpy/scipy). Dizer o que o teste de normalidade tem a ver com este item.

Desenvolvimento
---------------

Algoritmos implementados em Python. Para executar, basta digitar no terminal:

    $ python main.py

O código carregará todos os datasets e fará os testes compartivos de
agrupamento com K-means e K-means++ e mostrará os boxplot da quantidade de
iterações até a convergência.

Referências para implementação:

- http://stackoverflow.com/a/2605234/255258
- http://ilpubs.stanford.edu:8090/778/1/2006-13.pdf

Testes de normalidade
---------------------

Função utilizada: scipy.stats.mstats.normaltest (http://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.stats.mstats.normaltest.html)

### Base: Ruspini. (http://www.unc.edu/~rls/)

p-value (1a coluna): 0.02
p-value (2a coluna): 1.2e-09

### Base User Identification From Walking Activity (https://archive.ics.uci.edu/ml/datasets/User+Identification+From+Walking+Activity)

p-value (1a coluna): pvalue=3.45e-125 
p-value (2a coluna): pvalue=3.45e-34
