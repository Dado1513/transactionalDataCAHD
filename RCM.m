%% primo esempio
clc
close all
clear
table = csvread('data.csv');
subplot(1,2,1),spy(table),title('table')
p = symrcm(table);
R = table(p,p);
subplot(1,2,2),spy(R),title('table(p,p)')

[i,j] = find(table);
bw = max(i-j) + 1;


[i,j] = find(R);
bw_rcm = max(i-j) + 1;

fprintf(' %d-bandwidth original table \n',bw);
fprintf(' %d-bandwidth band table\n',bw_rcm);
%% secondo test con matrice complete
close all
clc 
clear
table = csvread('data_complete.csv');
subplot(1,2,1),spy(table),title('table')
p = symrcm(table);
R = table(p,p);
subplot(1,2,2),spy(R),title('table(p,p)')

[i,j] = find(table);
bw = max(i-j) + 1;


[i,j] = find(R);
bw_rcm = max(i-j) + 1;

fprintf(' %d-bandwidth original table \n',bw);
fprintf(' %d-bandwidth band table\n',bw_rcm);
