dados = dlmread('dataset/block_1.csv', ',', 2);
dados_teste = dlmread('dataset/block_2.csv', ',', 2);
dados_teste = vertcat(dados_teste, dlmread('dataset/block_3.csv', ',', 2));
dados_teste = vertcat(dados_teste, dlmread('dataset/block_4.csv', ',', 2));
dados_teste = vertcat(dados_teste, dlmread('dataset/block_5.csv', ',', 2));
dados_teste = vertcat(dados_teste, dlmread('dataset/block_6.csv', ',', 2));
dados_teste = vertcat(dados_teste, dlmread('dataset/block_7.csv', ',', 2));
dados_teste = vertcat(dados_teste, dlmread('dataset/block_8.csv', ',', 2));
dados_teste = vertcat(dados_teste, dlmread('dataset/block_9.csv', ',', 2));
dados_teste = vertcat(dados_teste, dlmread('dataset/block_10.csv', ',', 2));

X = dados(:,3:11);
Yd = dados(:,12);
Xteste = dados_teste(:,3:11);
Ydteste = dados_teste(:,12);

net = feedforwardnet(16);
[net1m, tr1m] = train(net, X', Yd');
Yteste = net1m(Xteste');
resultado = sum(Ydteste-Yteste');