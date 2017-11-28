%% test with table truncade online transactional
clc
close all
clear
table = csvread('online_retail_transaction.csv');
table_truncade = table(1:4000,1:4000);

subplot(1,2,1),spy(table_truncade),title('table')
p = symrcm(table_truncade);
R = table(p,p);
subplot(1,2,2),spy(R),title('table(p,p)')

[i,j] = find(table_truncade);
bw = max(i-j) + 1;


[i,j] = find(R);
bw_rcm = max(i-j) + 1;

fprintf(' %d-bandwidth original table \n',bw);
fprintf(' %d-bandwidth band table\n',bw_rcm);

