dados = dlmread('dados_3.txt');
X = dados(:,1:4);
Yd = dados(:,5:7);
NUM_EPOCHS = 100000;

net1 = feedforwardnet(15);
net2 = feedforwardnet(15);
net3 = feedforwardnet(15);
net4 = feedforwardnet(15);
net5 = feedforwardnet(15);

net1.trainParam.goal = 1e-6;
net2.trainParam.goal = 1e-6;
net3.trainParam.goal = 1e-6;
net4.trainParam.goal = 1e-6;
net5.trainParam.goal = 1e-6;

net1.trainParam.epochs = NUM_EPOCHS;
net2.trainParam.epochs = NUM_EPOCHS;
net3.trainParam.epochs = NUM_EPOCHS;
net4.trainParam.epochs = NUM_EPOCHS;
net5.trainParam.epochs = NUM_EPOCHS;

net1.trainParam.lr = 0.1;
net2.trainParam.lr = 0.1;
net3.trainParam.lr = 0.1;
net4.trainParam.lr = 0.1;
net5.trainParam.lr = 0.1;

[net1, tr1] = traingd(net1, X', Yd');
[net2, tr2] = traingd(net2, X', Yd');
[net3, tr3] = traingd(net3, X', Yd');
[net4, tr4] = traingd(net4, X', Yd');
[net5, tr5] = traingd(net5, X', Yd');

net1m = feedforwardnet(15);
net2m = feedforwardnet(15);
net3m = feedforwardnet(15);
net4m = feedforwardnet(15);
net5m = feedforwardnet(15);

net1m.trainParam.lr = 0.1;
net2m.trainParam.lr = 0.1;
net3m.trainParam.lr = 0.1;
net4m.trainParam.lr = 0.1;
net5m.trainParam.lr = 0.1;

net1m.trainParam.epochs = NUM_EPOCHS;
net2m.trainParam.epochs = NUM_EPOCHS;
net3m.trainParam.epochs = NUM_EPOCHS;
net4m.trainParam.epochs = NUM_EPOCHS;
net5m.trainParam.epochs = NUM_EPOCHS;

[net1m, tr1m] = traingdx(net1m, X', Yd');
[net2m, tr2m] = traingdx(net2m, X', Yd');
[net3m, tr3m] = traingdx(net3m, X', Yd');
[net4m, tr4m] = traingdx(net4m, X', Yd');
[net5m, tr5m] = traingdx(net5m, X', Yd');