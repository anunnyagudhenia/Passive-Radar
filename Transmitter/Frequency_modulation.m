%% Clear workspace
clear; clc; close all;


A0 = 1.0;      
B0 = 1.0;
fc = 100e6;        % carrier frequency (Hz)
fa = 1e6;          % message frequency (Hz)
fs = 500e6;        % sampling rate (Hz)
T1 = 1e-7;         
T2 = 20e-7;        

t1 = 0:1/fs:4*T1;
t2 = 4*T1:1/fs:8*T1;
t_FM = 0:1/fs:T2;

wc = 2*pi*fc;
wa = 2*pi*fa;


B1 = B0 * sin(wa*t1);
B2 = B0 * sin(wa*t2);
B_FM = B0 * sin(wa*t_FM);


transmitted_signal1 = A0 * sin(wc*t1 + B1);
transmitted_signal2 = A0 * sin(wc*t2 + B2);
FM_signal = A0 * sin(wc*t_FM + B_FM);

N = length(FM_signal);
X = fft(FM_signal);
f = (0:N-1)*(fs/N); 


figure('Position',[100 100 1400 500]);


subplot(1,3,1);
hold on;
plot(t1, A0*sin(wc*t1), 'r');         % carrier
plot(t1, transmitted_signal1, 'b');    % modulated
plot(t1, B1, 'g');                     % audio
hold off;
xlabel('Time (s)');
ylabel('Amplitude');
title('Interval 0 to 4T');
grid on;


subplot(1,3,2);
hold on;
plot(t2, A0*sin(wc*t2), 'r');         
plot(t2, transmitted_signal2, 'b');    
plot(t2, B2, 'g');                     
hold off;
xlabel('Time (s)');
ylabel('Amplitude');
title('Interval 4T to 8T');
grid on;

subplot(1,3,3);
plot(f/1e6, abs(X),'b');
xlabel('Frequency (MHz)');
ylabel('|X(f)|');
title('FM Signal (Frequency Domain)');
xlim([80 120]);   
grid on;
