Anotações sobre o sistema de pontes rolantes
============================================

- Pontes A e B podem ir para qualquer lugar;
- Ponte C só vai do centro até os lingotamentos;
- Não é necessário uma ponte para ir do convertedor (CV) até o borbulhamento (BO);



Forma de funcionamento da máquina de estados
--------------------------------------------

A máquina de estados vai receber uma série de transições e vai executa-las. O
problema é que essas transições não são automáticas e demoram um tempo para
serem executadas e ainda estão sujeitas à restrições temporais.

Para um funcionamento "ótimo" da máquina de estados, o seguinte pseudocódigo
recursivo de execução deve ser adotado. O procedimento "tick" será executado
quando nenhuma outra ponte puder ser movimentada na rodada em questão.

- A transição pode ter origem nula (entrando no CV) ou saída nula (saindo dos
  lingotamentos), mas nunca ambos nulos
- Se a transição tiver uma fonte, significa que ela tem que pegar a O.S em um
  estágio. E isso estará sujeito à verificação de completude do estágio.

- Para cada transição na fila de execução:
    - Enquanto a transição não for executada:
        - A ponte da transição pode executar trabalho?
            - Sim
                - Executa trabalho
            - Não
                - Alguma ponte das próximas transições pode executar trabalho?
                    - Sim
                        - Executa trabalho
                    - Não
                        - Tick

Procedimento "pode executar trabalho":
    - A ponte em questão está em movimento?
        - Sim
            - Então não pode executar trabalho
        - Não
            - A direção do movimento vai de encontro com a movimentação de alguma outra ponte?
                - Sim
                    - Então não pode executar trabalho
                - Não
                    - A ponte vai transportar alguma O.S?
                        - Sim
                            - A O.S está pronta?
                                - Sim
                                    - Então pode executar trabalho
                                - Não
                                    - Então não pode executar trabalho
                        - Não
                            - Pode executar trabalho

Procedimento "executar trabalho": 
    """
    Assumo aqui que já se sabe que a ponte pode executar o trabalho, então
    pularei esta verificação
    """
    - Coloque em movimento as pontes no meio do caminho, se houver;
    - Coloque a ponte em questão em movimento.

Procedimento Tick:
    - Dado o estado das pontes que estão em execução e dos fornos que estão
      executando algum trabalho, obter o menor tempo para completar.
    - Somar esse tempo na aciaria e diminuir de todos os tempos para completar
      pontos em execução (fornos e pontes).
    - Para todos os trabalhos concluídos
        - Coloca objeto (ponte ou forno) em questão como parado.
