% Clear workspace
clear; clc; close all;

% Parameters
A0 = 1.0;              % amplitude
fc = 1000;             % carrier frequency (Hz)
c  = 3e8;              % speed of light (m/s)
Rt = 10000;            % distance between transmitter and object (m)
Rr = 10000;            % distance between receiver and object (m)
fs = 1e6;              % sampling rate (Hz)
T  = 0.001;            % signal duration (s)

% Time vector
t = 0:1/fs:T;

% Frequency for audio signal
fa = 100;  

% Transmitted signal (modulated)
s = A0 * sin(((2*pi*fc) + (2*pi*fa)) .* t);

% Delay
R = Rt + Rr;
tau = R / c;

% Received signal (with delay)
r = A0 * sin(((2*pi*fc) + (2*pi*fa)) .* t + (2*pi*fc*tau));

% --- Plot ---
figure('Position',[100 100 900 400]);
plot(t, s, 'b', 'LineWidth', 1.2); hold on;
plot(t, r, 'r--', 'LineWidth', 1.2);
xlabel('Time');
ylabel('Amplitude');
legend('Transmitted signal','Received signal (delayed)');
grid on;
title('Transmitted vs Received Signal');
