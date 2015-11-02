Executando os testes
--------------------

Configuração necessária: Ubuntu Linux 14.04 (mínimo).

Não é necessário instalar nenhuma dependência de antemão, bastando executar o
seguinte comando para iniciar os testes:

    make run

O makefile se encarregará de instalar as dependências faltantes e executar os
testes. Ao final de cada uma das 100 iterações do teste, um arquivo JSON com os
resultados será criado.

Caso algo aconteça durante a execução dos testes e o comando encerre, basta
executar novamente o comando acima que os testes serão continuados do ponto que
pararam.
