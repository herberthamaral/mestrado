%trabalho prático II - Herberth Amaral
dados = dlmread('dados_2.txt');
dados_teste = dlmread('dados_ex5.txt');
X = dados(:,1:3);
Yd = dados(:,4);
Xteste = dados_teste(:,1:3);
Ydteste = dados_teste(:,4);
[net1, tr1] = traingdx(feedforwardnet(10), X', Yd');
[net2, tr2] = traingdx(feedforwardnet(10), X', Yd');
[net3, tr3] = traingdx(feedforwardnet(10), X', Yd');
[net4, tr4] = traingdx(feedforwardnet(10), X', Yd');
[net5, tr5] = traingdx(feedforwardnet(10), X', Yd');
 
disp('Erro quadrático médio - T1')
disp(tr1.best_perf)
disp('Num. epocas - T1')
disp(tr1.num_epochs)
disp('Y - T1')
disp(net1(Xteste')')
disp('Erro relativo medio T1')
disp((abs(Ydteste' - net1(Xteste'))/Ydteste')*100)
disp('Variância - T1')
disp(var(Ydteste' - net1(Xteste'))*100);
 
disp('Erro quadrático médio - T2')
disp(tr2.best_perf)
disp('Num. epocas - T2')
disp(tr2.num_epochs)
disp('Y - T2')
disp(net2(Xteste')')
disp('Erro relativo medio T2')
disp((abs(Ydteste' - net2(Xteste'))/Ydteste')*100)
disp('Variância - T2')
disp(var(Ydteste' - net2(Xteste'))*100);
 
disp('Erro quadrático médio - T2')
disp(tr3.best_perf)
disp('Num. epocas - T2')
disp(tr3.num_epochs)
disp('Y - T3')
disp(net3(Xteste')')
disp('Erro relativo medio T3')
disp((abs(Ydteste' - net3(Xteste'))/Ydteste')*100)
disp('Variância - T3')
disp(var(Ydteste' - net3(Xteste'))*100)
 
disp('Erro quadrático médio - T3')
disp(tr4.best_perf)
disp('Num. epocas - T3')
disp(tr4.num_epochs)
disp('Y - T4')
disp(net4(Xteste')')
disp('Erro relativo medio T4')
disp((abs(Ydteste' - net4(Xteste'))/Ydteste')*100)
disp('Variância - T4')
disp(var(Ydteste' - net4(Xteste'))*100)
 
disp('Erro quadrático médio - T5')
disp(tr5.best_perf)
disp('Num. epocas - T5')
disp(tr5.num_epochs)
disp('Y - T5')
disp(net5(Xteste')')
disp('Erro relativo medio T5')
disp((abs(Ydteste' - net5(Xteste'))/Ydteste')*100)
disp('Variância - T5')
disp(var(Ydteste' - net5(Xteste'))*100)