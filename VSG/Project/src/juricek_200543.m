%% INFO / Task 1
% !Note: Make sure you have the addon: Signal Processing Toolbox
% In /src is also saved workspace as file "juricek_200543.mat"

clc;
clear;
close all;

% print basic info header
fprintf('---------------------------------\n');
fprintf('[INFO] VUT ID: 200543\n');
fprintf('[INFO] Author: Martin Juricek\n');
fprintf('[INFO] IACS FME BUT @2021\n');
fprintf('---------------------------------\n');

% read specified audio file from assignment
[s, Fs] = audioread('../audio/200543.wav');

% play loaded audio
sound(s, Fs)

% get signal as row vector
s = s';

% length of samples
len_samples = length(s);

% length in seconds
len_seconds = len_samples/Fs;

% maximum of signal
max_s = max(s);

% minimum of signal
min_s = min(s);

% print infos
fprintf('[INFO] Length of samples: %i\n',len_samples);
fprintf('[INFO] Length in sec: %.2f\n',len_seconds);
fprintf('[INFO] Max: %.2f\n',max_s);
fprintf('[INFO] Min: %.2f\n',min_s);

% time to sample
t = (0:len_samples-1)/Fs;

% plot figure - loaded audio
figure(1)
plot(t, s)
title('Input signal');
xlabel('t [s]');
xlim([-0.1 len_seconds+0.1]);
ylim([min_s-0.01 max_s+0.01]);

%% Task 2 

% length of samples
N = 1024;

% overlap
S = 512;

% centering signal
s_cent = s-mean(s);

% normaliazing signal
s_norm = s_cent/abs(max_s);

% split norm. signal to frames to 1024 with oversampling 512
frames = buffer(s_norm,N,S)';
t_frames = buffer(t,N,S,'nodelay')';

% choose "nice" frame(choosen vowel: i): 6
c_f = 41;

figure(2)
subplot(2,1,1);
plot(t, s_norm);
hold on;
plot(t_frames(c_f,:),frames(c_f,:),'r');
xlim([-0.1 len_seconds+0.1]);
xline(1.28,'r','LineWidth',2);
title('Serach "Nice" sounded signal vowel: e');
hold off;

% plot figure - sounded frame
subplot(2,1,2);
plot(t_frames(c_f,:),frames(c_f,:),'r','LineWidth',2);
title('"Nice" sounded signal frame');
xlabel('t [s]');
xlim([t_frames(c_f,1)-0.005 t_frames(c_f,end)+0.005]);
ylim([-1 1])

%% Task 3

% get sounded signal frame
sig = frames(c_f,:);

% compute dft
% start timer
tic;
trans_s = dft(sig,N);
% get time
toc

% compute fft to compare
% start timer
tic;
comp_s = fft(sig);
% get time
toc

% get frequencies
f = (0:length(trans_s)-1)/length(trans_s)*Fs;

% plot DFT
figure(3)
subplot(2,1,1);
stem(f, abs(trans_s), 'b');
grid on;
title('DFT module');
xlabel('frequency [Hz]');
xlim([0 Fs/2]);

% visual compare FFT
subplot(2,1,2);
stem(f,abs(trans_s),'b');
hold on;
stem(f, abs(comp_s),'r');

grid on;
title('FFT module');
xlabel('frequency [Hz]');
xlim([0 Fs/2]);

legend({'DFT','FFT'});
hold off;

%% Task 4

% compute and plot spectrogram
[sgr,f_sgr,t_sgr] = spectrogram(s_norm,N,S,[],Fs);
P = 10*log10(1/N*abs(sgr).^2);

figure(4)
pcolor(t_sgr,f_sgr,P);
shading flat;
z = colorbar;
title('Signal spectrogram');
ylabel(z,'power spectral density [dB]');
xlabel('t [s]');
ylabel('frequency [Hz]');
axis tight;
colormap(jet);

%% Task 5

% subtraction from the spectrogram
f1 = 690;
f2 = 1380;
f3 = 2070;
f4 = 2740;

%% Task 6

% def time vector
t_c = (0:1/Fs:len_seconds-1);

% create combination of 4 disturbing cos 
cos_out = cos(2*pi*f1*t_c) + cos(2*pi*f2*t_c) + cos(2*pi*f3*t_c) + cos(2*pi*f4*t_c);

% write audio file
audiowrite('../audio/4cos.wav',cos_out,Fs,'BitsPerSample',16);

% play audio
sound(cos_out,Fs)

% plot spectrogram
[sgr,f_sgr,t_sgr] = spectrogram(cos_out,N,S,[],Fs);
P = 10 * log10(1/N*abs(sgr).^2);

figure(6)
pcolor(t_sgr,f_sgr,P);
shading flat;
z = colorbar;
title('Disturbing cosines spectrogram');
ylabel(z,'power spectral density [dB]');
xlabel('t [s]');
ylabel('frequency [Hz]');
axis tight;
colormap(jet);

%% Task 7, 8, 9, 10

% designe filter and do filtration
freq = [f1,f2,f3,f4];
[s_filtred,z,p,b,a] = four_filters(freq,Fs,s_norm);

%% Task 8

% plot poles - zeros
figure(8)
for i=1:length(freq)
    subplot(length(freq),1,i);
    zplane(z(:,i),p(:,i));
    title(['Zeros and poles: filter n. ',num2str(i)]);
end

%% Task 9

% plot frequency characteristics for each filter
% !! in protocol wrong freq. char. !!
% Correction by: https://nbviewer.org/github/zmolikova/ISS_project_study_phase/blob/master/Zvuk_spektra_filtrace.ipynb

for i=1:length(freq)
    [h,w] = freqz(b(i,:),a(i,:));
    subplot(length(freq),1,i);
    plot(w / 2 / pi * Fs/2, abs(h), 'LineWidth', 2)
    title(['Filter n.', num2str(i),' freq. char. module |H(e^{j\omega})|'])
    xlim([0 + i*150 350 + i*300]);
    xlabel('Frequency [Hz]');
end

%% Task 10

% plot filtrated signal
figure(20)
plot(t,s_filtred);
title('Filtred signal');
xlabel('t [s]');
xlim([-0.1 len_seconds+0.1]);

% play filtred signal
sound(s_filtred,Fs)

% write filtred signal
audiowrite('../audio/clean_bandstop.wav',s_filtred,Fs,'BitsPerSample',16);

%%

% plot spectrogram of filtred signal for visual validation of filtration
figure(21)
[sgr,f_sgr,t_sgr] = spectrogram(s_filtred,N,S,[],Fs);
P = 10*log10(1/N*abs(sgr).^2);

pcolor(t_sgr,f_sgr,P);
shading flat;
z = colorbar;
title('Filtred signal spectrogram');
ylabel(z,'power spectral density [dB]');
xlabel('t [s]');
ylabel('frequency [Hz]');
axis tight;
colormap(jet);

%% Functions

% public function:
%   input: normalised signal, length of samples
%   return: transormated signal
% Note: Computitaion is based on matrix multiplication bases with the
% signal vector.
function [trans_s] = dft(s,N)
    mat_B = dftmtx(N);
    trans_s = s*mat_B;
end

% public function:
%   input: vector of frequencies, sampling frequency, normalised signal
%   return: filtred signal, matrix of zeros, matrix of poles, matrix of
%   coef. b, matrix of coef. a
% Note: In the function, the design, construction and actual filtering is 
% performed in a for loop. The basic parameters are defined(such passband 
% ripple, etc..) and the function p_imp is called to print coeficients of 
% filters and plot the graph impulse characetrics. 
function [s,z_s,p_s,b_s,a_s] = four_filters(f,Fs,y)
    % Nyquist frequency    
    Fn = Fs/2;
    % passband ripple
    Rp = 3;
    % passband ripple
    Rs = 40;
    
    % pre alocated vector of coef.
    z_s = zeros(14,length(f));
    p_s = zeros(14,length(f));

    a_s = zeros(length(f),15);
    b_s = zeros(length(f),15);

    for i=1:length(f)
        % stopband frequency
        Wp = [f(i)-25 f(i)+25]/Fn;
        
        % passband frequency
        Ws = [f(i)-50 f(i)+50]/Fn;
        
        % Butterworth filter order and cutoff frequency calculation
        [n,Wp] = buttord(Wp,Ws,Rp,Rs);
        
        % Butterworth filter design: Zero-Pole-Gain
        [z,p,k] = butter(n,Wp,'stop');
        
        z_s(:,i) = z;
        p_s(:,i) = p;

        % convert zero-pole-gain filter parameters
        [b,a] = zp2tf(z,p,k);
        
        b_s(i,:) = b;
        a_s(i,:) = a;
        
        % plot and print
        p_impz(b,a,f,i);

        % convert zero-pole-gain filter parameters to second-srder section 
        % for stability
        [sos,g] = zp2sos(z,p,k);
        
        % filter signal
        if i == 1
            s = filtfilt(sos,g,y);
        else
            s = filtfilt(sos,g,s);
        end
    end
end

% public function:
%   input: vector coef. b, vector coef. a, vector of freq, state in loop
%   loop
%   return: 
% Note: Plot impulse characteristics and print coef. of filters
function p_impz(b,a,f,i)
    figure(7)
    subplot(length(f),1,i);
    
    % Impulse response of discrete-time filter
    [h, t] = impz(b,a,50);
    scatter(t,h,15,'filled');
    title(['Impulse response frequency ',num2str(f(i)),' [Hz]']);
    xlabel('samples');

    fprintf("[INFO] Coeficients of filter for frequency %i [HZ]\n",f(i));
    fprintf("[INFO] [b] = [");
    fprintf(' %.2g ',b);
    fprintf(']\n');
    fprintf("[INFO] [a] = [");
    fprintf(' %.2g ',a);
    fprintf(']\n');
    fprintf('\n');
end
