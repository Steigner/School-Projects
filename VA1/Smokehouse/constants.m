clc;
clear;

% meat / sausage heat capacity factor
Ck = 2.34;

% air
Cvu = 0.11;
Cvo = 0.11;

% concrete from expanded slate
Cu = 0.880;
Co = 0.880;

% coefficient of thermal resistance
% air of smokehouse - smokehouse
R1 = 0.625 + 34.61;

% air of smoke - air of fire
R2 = 34.61 + 11.54;

% air chimneys - air around the chimney
R3 = 34.61 + 115.54; %12.08 + 34.61;

% smokehouse - air around
R4 = 0.625 + 115.54;

% air fireplace - ohniste
R5 = 11.54 + 0.416;

% fireplace - air around
R6 = 0.416 + 115.4;

% smoked meat / sausage - air smokers
R7 = 34.61 + 0.29;

% air of fire - air around
R8 = 11.54 + 115.54;