A fuzzy logic intelligent agent for information extraction: introducing a new fuzzy logic-based term weighting scheme
=====================================================================================================================


Introdução
----------

O artigo fala basicamente de um sistema de inferência fuzzy utilizado para
melhorar os resultados de buscas dentro do portal da universidade de Servilha,
na Espanha.

O sistema de inferência fuzzy previamente mencionado foi criado para
classificar o nível de pertinência de páginas web dado uma busca feita por um
perfil de usuário. O nível de pertinência também pode ser chamado de relevância
da busca.

Um outro sistema fuzzy foi utilizado para substituir um algoritmo padrão de
"pesagem" de palavras chave, com o intuito de  melhorar a classificação de
palavras-chave em documentos.

Como as informações de busca são vagas e imprecisas, o motor de inferência
fuzzy, aliado com técnicas de recuperação de informação e processamento de
linguagem natural, foi capaz de entregar bons resultados.

Problema
--------

O principal problema tratado no artigo é: dado uma base de dados
não-estruturada (páginas web, por exemplo), como realizar buscas semânticas
provendo resultados relevantes?

O objeto do problema é o website da universidade de Servilha, na Espanha. A
intenção é criar um robô atendente que responde perguntas de visitantes da
página.

Referencial teórico
-------------------

### VSM

O VSM é um modelo algébrico de similaridade de texto muito usado na indústria
para criar soluções de buscas textuais, como o Lucene.

No VSM, o texto passa por três fases:

- Indexação do documento, onde os termos mais relevantes são exatraídos;
- Adição de pesos (term weighting) ao índice - tarefa geralmente feita pelo
  algoritmo TF-IDF (Term frequency-inverse document frequency);
- Classificação de acordo com a medida de similaridade.

A busca, então, é feita com base nas palavras chaves indexadas e nos seus
respectivos pesos.

### TF-IDF

O algoritmo TF-IDF (term frequency-inverse document frequency) é uma medida
estatística que tem o intuito de indicar a importância de uma palavra ou termo
de um documento em relação a uma coleção de documentos.

TF (term frequency) diz respeito à frequencia de um termo no documento. Quanto
mais vezes um termo aparecer em um documento, maior o seu peso. No entanto,
essa abordagem inocente dá um valor muito alto para "stop-words" (artigos,
preposições, etc).

Para resolver o problema do TF, o IDF (inverse document frequency) preocupa-se
em analisar a frequencia das palavras chave em um conjunto de documentos, de
forma que as palavras mais frequentes em todos os documentos são rebaixadas.

Além da contribuição inicial, o presente trabalho provê uma alternativa fuzzy
ao TF-IDF.

### Recuperação e extração de informações

A recuperação de informações é a busca automática de informações relevantes
contidas num conjunto de conhecimento que levam em conta duas características
chave: recall e precisão.  O recall é a proporção de objetos relevantes
encontrados em relação a todos os objetos relevantes, enquanto que a precisão
diz respeito à proporção de objetos relevantes retornados na busca.

Os dois conceitos são diferentes e um pode existir sem o outro. Exemplo: uma
busca que retorna todas as páginas como relevantes tem um recall alto porque
não deixou nenhuma relevante de fora. No entanto, possui uma precisão baixa por
conter muitos resultados não-relevantes. Da mesma forma, uma busca que retornou
apenas um resultado relevante quando há mais resultados relevantes possui uma
precisão alta, pois não há erros, mas possui um recall baixo porque deixou
resultados relevantes de fora. Uma boa precisão e um bom recall fazem parte de
um bom sistema de recuperação de informações.

A informação precisa ser extraída depois da informação ser recuperada de forma
automática. O problema é a extração de pedaços de texto que respondem à
perguntas específicas. O rsultado deste processo é armazenado em um banco de
dados estruturado.

Técnicas de processamento de linguagem natural são usadas para melhorar o
recall e a precisão. O texto não dá muitos detalhes de como este processo é
feito.

Metodologia
-----------

Para que o robô consiga responder as perguntas, uma base de dados de
conhecimento precisa estar disponível para busca. Para isso, os autores
indexaram todas as páginas do site da universidade de Servilha de forma
hierárquica nesta ordem: tópico, seção, objeto. Cada objeto representa uma
única página e é possível associar mais de um objeto a uma mesma página se o
conteúdo da mesma for muito heterogêneo.

Para indexação foi usado o VSM juntamente com o TF-IDF para "pesagem" das
palavras-chave.

As entradas do sistema de inferência fuzzy são os pesos das palavras chaves da
busca.

Para este trabalho, os conjuntos de pertinência fuzzy são LOW, MEDIUM e HIGH,
modelados de forma triangular. A saída pode ser LOW, MEDIUM-LOW, MEDIUM-HIGH e
HIGH. Os valores dos conjuntos fuzzy são os seguintes:

- LOW: de 0.0 a 0.4, centrado em 0.0;
- MEDIUM: de 0.2 a 0.8, centrado em 0.5;
- HIGH: de 0.6 a 1.0, centrado em 1.

Esses valores representam o peso dos objetos resultantes da busca em relação ao
termo de busca. Exemplo: uma busca por "prazo de inscrição no vestibular" pode
considerar apenas 3 palavras-chave: prazo, inscrição e vestibular. Páginas que
contenham informações do vestibular possuem um peso alto para as palavras-chave
prazo, inscrição e vestibular, enquanto que páginas de contato, por exemplo,
tem pesos pequenos ou nulos. Desta forma, é possível obter os documentos que
possuem as palavras chave da busca para que então o motor de inferência fuzzy
dê o nível de pertinência do documento em relação aos termos da busca.

Os valores da saída são:

- LOW: de 0.0 a 0.4, centrado em 0.0;
- MEDIUM-LOW: de 0.1 a 0.7 centrado em 0.4;
- MEDIUM-HIGH: de 0.3 a 0.9, centrado em 0.6;
- HIGH: de 0.6 a 1.0, centrado em 1;

As regras do motor de inferência são as seguintes:

- Se uma das entradas é HIGH ENTÃO HIGH;
- Se todas as entradas são MEDIUM ENTÃO HIGH;
- Se duas entradas são MEDIUM a outra é LOW ENTÃO MEDIUM-HIGH;
- Se uma entrada é MEDIUM e as outras duas são LOW ENTÂO MEDIUM-LOW;
- Se todas as entradas são LOW então LOW.


### Alternativa ao TF-IDF

O TF-IDF funciona bem, mas possui a desvantagem de não considerar o grau de
identificação do objeto se somente o termo do índice considerado é usado e a
existência de palavras chaves compostas.

Por causa disso, os autores propuseram um sistema que leva em consideração não
apenas os cálculos TF e IDF, mas algumas outras variáveis importantes na
definição do peso da palavra-chave. No total, quatro pontos são levados em conta:

- Quão comum é uma palavra-chave aparecer em outros documentos? (IDF);
- Quão comum é uma palavra-chave aparecer no seu próprio documento? (TF);
- Uma palavra-chave indubitavelmente define um objeto por si só?;
- Uma palavra-chave está ligada com outra?

As respostas destas perguntas alimentam um sistema de inferência fuzzy chamado
Weight Assigner em que a saída deste sistema define o peso da palavra chave
correspondente para aquele documento.

Resultados
----------

Apesar do TF-IDF funcionar bem, os resultados do sistema fuzzy fizeram a
precisão do sistema aumentar de 50.98% para 77.68% no primeiro resultado da
busca, sem afetar o recall negativamente. Considerando os três primeiros
resultados, a precisão aumentou de 81.18% para 92.45%.

[inserir tabela 13]

Os testes mostraram que um sistema de inferência fuzzy de três variáveis para
classificação dos resultados da busca funcionaram melhor que um sistema de
inferência com cinco variáveis.
