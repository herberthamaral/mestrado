dados = dlmread('output.csv', ',');
dados_teste = dlmread('output-test.csv', ',');
disp(datestr(now));
fis = anfis(dados);
disp(datestr(now));
[linhas, colunas] = size(dados_teste);

num_erros = 0;
num_dif4 = 0;
num_linhas = 0;
for num_linha = 1:linhas
    num_linhas = num_linhas+1;
    linha = dados_teste(num_linha, 1:4);
    [l,c] = size(linha);
    if c ~= 4
        num_dif4 = num_dif4+1;
        continue
    end
    if round(evalfis(linha(1,1:3), fis)) ~= linha(4)
        num_erros = num_erros +1;
    end;
end;
disp('Total de erros: ')
disp(num_erros)
disp('Porcentagem de erros: ')
disp((num_erros/linhas)*100)
