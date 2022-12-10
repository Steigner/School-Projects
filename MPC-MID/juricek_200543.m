% Description: This script identifies the defined nonlinear system that is generated 
% unique to the students in the course.
% Main approach:
% this .m script is use sections run. Global run, runs script with default
% settings.
%
% ! Important !: Due to section run approach, i assignment in every section
% vars(u,y,t). This allows you to skip sections. In section approach i usually 
% assigment only vectors that i will use in defined context.
%
% I use a representation of this vars as:
%   y = output signal
%   u = input signal
%   t = time
% 
% Note: Identification toolbox is not supported in Matlab Online version. 

clc;
clear;
close all;

% print basic info header
fprintf('---------------------------------\n');
fprintf('[INFO] VUT ID: 200543\n');
fprintf('[INFO] Author: Martin Juricek\n');
fprintf('[INFO] IACS FME BUT @2021\n');
fprintf('---------------------------------\n');

% VUT personal ID
ID = 200543;

% defualt determined amplitude value to PRBS
% a = 0.9;

% load prepared data from identification amplitude
load('ampl_ident.mat');

%% IDENTIFICATION AMPLITUDE FOR INPUT PRBS SIGNAL

% % time-step
% t = 0:0.1:2000;
% 
% % amplification 
% P = 0.001*t;
% 
% % output signal
% y = odezva_2021(ID, P ,t);
% 
% % reverse normalization
% t = t / 1000;
% 
% % plot -> find amplitude for PRBS signal
% figure(101)
% plot(t,y,'b');
%
% set amplitude from graph
% a = 0.9;
% save('ampl_ident.mat')

%% I/O SYSTEM

% period - circa 10% of ramp-up time
Ts = 4;

% time vector
t = 0:Ts:4500;

% get size of t vector
[~, N] = size(t); 

% Split data to:
%   1) identification - 75%
%   2) testing - 20%
%      - 10% positive step
%      - 10% negative step
%   3) delay - 5%
N_ident = round(0.75 * N);
N_step = round(0.2 * N);
N_zeros = N - N_ident - N_step;

% input PRBS signal - limited
u_prbs = idinput(N_ident, 'prbs', [0 0.08], [-a a]);

% validation data split
N_split = round(N_step/2);

% step response(testing/validation) u [pos neg]
u_step = [ones(N_split,1)*a; ones(N_step - N_split,1)*-a];

% delay u
u_zeros = zeros(N_zeros,1);

% merge u
u = [u_prbs' u_zeros' u_step'];

% output signal
y = odezva_2021(ID, u, t);

% get val. time vector of step
t_step = 0:1:N_step-1;

% validation output signal
y_step = y(end-N_step+1:end);

% get ident. time vector
t_ident = t(1:N_ident);

% identification output signal
y_ident = y(1:N_ident);

% splitters
t_s = t(end-N_step+1);
t_l = t(end-N_split);
t_i = t(N_ident);

% plot to figure 1
% 1 subplot - system response to input PRBS signal
figure(1)
subplot(3,1,1);
% output signal
plot(t,y,'b','LineWidth',1);
hold on;
% prbs signal
plot(t_ident,u_prbs,'LineWidth',1);
xlabel('t');
ylabel('y');
grid on;
title('System response to input PRBS signal');
% splitters
xline(t_s,'r','LineWidth',2);
xline(t_i,'r','LineWidth',2);
xline(t_l,'r','LineWidth',2);
legend('output signal','PRBS signal' ,'Location','NorthEast');
hold off;

% 2 subplot - system response to input steps
subplot(3,1,2);
plot(t_step,y_step,'b','LineWidth',1);
xlabel('step t');
ylabel('step y');
ylim([-5 5]);
grid on;
title('Step response');

% 3 subplot - identification output signal
subplot(3,1,3);
plot(t_ident,y_ident,'b','LineWidth',1);
xlabel('ident. t');
ylabel('ident. y');
grid on;
title('Identification response');

%% TRANSPORT DELAY DETECTION

y = y_ident;
u = u_prbs;

% call function Delay Transport Detection
d = DTD(u,y);

% print detected delay
fprintf('[INFO] Detected transport delay: d = %i', d);

%% DC COMPONENT

% visual identification -> output signal on input PRBS signal
% stationary DC component -> whole signal will be shifted in y axis
% non-stationary DC component -> modulation of signal, or shifted by
% angle/radian

% y = y_ident;
% u = u_prbs;

% % mean value of output signal and input prbs signal
% m_y = mean(y);
% m_u = mean(u);

% % compute corrections
% y_ = y - m_y;
% u_ = u - m_u;

%% LEAST SQUARE METHOD - DELAYED OBSERVATION

u = u_prbs;
y = y_ident;
t = t_ident;

% call least square method - delayed observation
TH1 = LSM_DO(u,y);

% prepare estimation vector and get estimated values
y1 = zeros(size(u));

% very ugly code, but to understand
% Note: further in the script is use same principle but with nicer code  
y1(1) = 0 + 0 - 0 - 0;
y1(2) = TH1(3)*u(1) + 0 - TH1(1)*y1(1) - 0;

for k = 3:length(u)
     y1(k) = TH1(3)*u(k-1) + TH1(4)*u(k-2) - TH1(1)*y1(k-1) - TH1(2)*y1(k-2);
end

% plot estimation and real output signal
figure(2)
plot(t,y,'r',t,y1,'b','LineWidth',1);
xlabel('t');
ylabel('y');
title('Least square method - delayed observation');
legend('real','LSM - delayed observation' ,'Location','NorthEast');

%% LEAST SQUARE METHOD - ADDITIONAL MODEL

u = u_prbs;
y = y_ident;
t = t_ident;

% call least square method - additional model
TH2 = LSM_AM(u,y);

% prepare estimation vector and get estimated values
y2 = zeros(size(u));
y2(1) = 0;
y2(2) = TH2(3)*u(1) - TH2(1)*y2(1);
for k = 3:length(u)
     y2(k) = TH2(3)*u(k-1) + TH2(4)*u(k-2) - TH2(1)*y2(k-1) - TH2(2)*y2(k-2);
end

% plot estimation and real output signal
figure(3)
plot(t,y,'r',t,y2,'b','LineWidth',1);
xlabel('t');
ylabel('y');
title('Least square method - additional model');
legend('real','LSM - addition model' ,'Location','NorthEast')

%% PLOT BOTH METHODS

% !! this is functional section only, if u run LMS methods sections !!
% plot estimated signal by both methods and real output signal
figure(4)
plot(t,y,'r',t,y2,'b',t, y1,'g','LineWidth',1);
xlabel('t');
ylabel('y');
title('Least square method - AM | DO');
legend('real','LSM - AM', 'LSM - DO','Location','NorthEast')

%% STEP RESPONSE

% !! choose which model you want to validate
% default set up - LMS DO
TH = TH1;

u = u_step;
t = t_step;

% prepare estimation vector and get estimated values to step
y_t = zeros(length(y_step),1);
y_t(1) = 0;
y_t(2) = TH(3)*u(1) - TH(1)*y_t(1);
for k = 3:length(y_step)
     y_t(k) = TH(3)*u(k-1) + TH(4)*u(k-2) - TH(1)*y_t(k-1) - TH(2)*y_t(k-2);
end

% plot estimation and real output signal to steps
figure(5)
plot(t,y_t,'b',t,y_step,'r','LineWidth',1);
xlabel('t');
ylabel('y');
title('Step response');
legend('estimation','real','Location','NorthEast');

%% FUNCTIONS

% public function:
%   input: vector of sys. input signal, vector of sys. output signal
%   return: theta vector
% Note: Least square method with auxiliary variables and delayed
% observation. Basically this method to the original LSM use just d step
% delay in output signal.
function th = LSM_DO(u,y)
    k = 5:length(u);
    
    % algo delay
    d = 2;
    
    % observation vector
    phi = [-y(k-1), -y(k-2), u(k-1), u(k-2)];

    % vector of delayed observations
    z = [-y(k-1-d), -y(k-2-d), u(k-1), u(k-2)];
    
    y_i = y(k);
    
    % call segmentation function
    [y_i,phi,z] = segmentation(y_i,phi,z);
    
    % calculate theta params [b a]
    th = (z'*phi)\(z'*y_i);
end

% public function:
%   input: vector of sys. input signal, vector of sys. output signal
%   return: theta vector
% Note: Least square method with auxiliary variables and additional model.
% This method compute first LMS, which we denote as additional model and 
% then use this model as input, which will refine the calculation.
function th = LSM_AM(u,y)
    % determination of initial parameters by classical LMS
    k = 3:length(u);
    Y = y(k);

    % auxiliary parameters pthi and theta
    phi_ivm = [-y(k-1),-y(k-2), u(k-1) ,u(k-2)];
    th_ivm = phi_ivm \ Y;
    
    y_ivm = zeros(size(u));
    for k = 3:length(u)
        y_ivm(k) = th_ivm(3)*u(k-1) + th_ivm(4)*u(k-2) - th_ivm(1)*y_ivm(k-1) - th_ivm(2)*y_ivm(k-2);
    end
    
    k = 3:length(u);
    
    % calculation with additional model 
    phi = [-y(k-1),-y(k-2), u(k-1) ,u(k-2)];
    z = [-y_ivm(k-1),-y_ivm(k-2), u(k-1) ,u(k-2)];
    y_i = y(k);
    
    % call segmentation function
    [y_i,phi,z] = segmentation(y_i,phi,z);
    
    % calculate theta params [b a]
    th = (z'*phi)\(z'*y_i);
end

% public function:
%   input: vector output signal, vector of phi, vector of aux. z 
%   return: segm. vector input signal, vector of phi, vector of aux. z 
% Note: Simple segmentation by method "smart scratch off". This method scratches the whole blackout even with 
% a relative hit to elements in equations.
function [y,phi,z] = segmentation(y,phi,z)
    % smart scratch off
    s = find(y == 0);
    k = zeros(length(s)*3,1);
    for i=1:3
        k = [s; s+i];
    end 
    % delete blackout
    % Note: It is necessary to limit deletion, becouse if output identification
    % sig. ended with blackout, then our method want to delete elements
    % with indexes out from vector. 
    y(k(k <= length(y))) = [];
    phi(k(k <= length(phi)),:) = [];
    z(k(k <= length(z)),:) = [];
end

% public function:
%   input: vector sys. input signal, vector sys. output signal
%   return: delay d
% Note: Identification delay of this system: First compute recursive method
% of LMS, the we check if delay from first abs. b is less then abs. in k
% steps.
function d = DTD(u,y)
    % recursive least squares method
    % init covariance matrix    
    P = 1e5*eye(4,4);      

    % init vector unknown parameters
    th = [0 0 1 0]';
    
    % preparation of the output parameter matrix
    TH = zeros(4,length(u)); 
    TH(:,1) = th; 
    TH(:,2) = th;

    for k = 3:length(u)
        % calculation of phi for the current step
        phi = [-y(k-1), -y(k-2), u(k-1), u(k-2)]';
        % calculation of the deviation
        e = y(k) - phi'*th;
        % calculation of correction
        K = P*phi /  (1 + phi'*P*phi);
        % updating the covariance matrix
        P = P - K*phi'*P;
        % calculation of parameter estimates in the current step
        th = th + K * e;
        TH(:,k) = th;                                
    end
    
    % get vector of B
    b = TH(3,:);
    
    % detection transpor delay
    % init transport delay
    d = 0;
    
    % check delay in first step
    if(abs(b(1)) < 0.15 * abs(b(2)))
        b(1) = 0;
        d = 1;
    end
    
    % check delay for all b(k)
    for k = 2:length(u)-1
        if(abs(b(1)) < 0.15 * abs(b(k+1)))
            d = k + 1;
        end
    end
end
