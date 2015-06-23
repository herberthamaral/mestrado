a=newfis('a')
a=addvar(a,'input','pressaoentrada',[0 100]);
a=addvar(a,'input','vazao',[0 100]);
a=addvar(a,'output','pressaosaida',[0 100]);
a=addmf(a,'input',1,'baixo','gaussmf',[15 0]);
a=addmf(a,'input',1,'medio','gaussmf',[15 50]);
a=addmf(a,'input',1,'alto','gaussmf',[15 100]);
a=addmf(a,'input',2,'baixo','trimf',[0 0 50]);
a=addmf(a,'input',2,'medio','trimf',[0 50 100]);
a=addmf(a,'input',2,'alto','trimf',[50 100 100]);
a=addmf(a,'output',1,'baixo','trimf',[0 0 0]);
a=addmf(a,'output',1,'medio','trimf',[50 50 50]);
a=addmf(a,'output',1,'alto','trimf',[100 100 100]);
plotmf(a,'input',1)
pause
close
plotmf(a,'input',2)
pause
close
plotmf(a,'output',1)
pause
close
ruleList=[
    	1 1 1 1 1
    	1 2 1 1 1
        1 3 2 1 1
        2 1 1 1 1
        2 2 2 1 1
        2 3 3 1 1
        3 1 2 1 1
        3 2 3 1 1
        3 3 3 1 1];
    a = addrule(a,ruleList);
    showrule(a)
    pause
    x1=input('entre com a pressao de entrada, pe = ');
    x2=input('entre com a vazao, q = ');
    z=evalfis([x1 x2],a)