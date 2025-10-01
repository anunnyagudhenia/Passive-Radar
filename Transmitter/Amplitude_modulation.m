% Clear workspace
clear; clc; close all;

% Parameters
A0 = 1.0;              % amplitude
fc = 100e6;            % carrier frequency (Hz)
fa = 1e6;              % audio frequency (Hz)
fs = 500e6;            % sampling frequency (Hz)
T  = 1e-6;             % signal duration (s)

% Time vector
t = 0:1/fs:T;


wc = 2*pi*fc;
wa = 2*pi*fa;

B = sin(wa*t);

carrier = A0 * sin(wc*t);

transmitted_signal = B .* carrier;

N = length(transmitted_signal);
X = fft(transmitted_signal);
f = (0:N-1)*(fs/N);



figure('Position',[100 100 1200 500]);

% (1) Time domain signals
subplot(1,2,1);
hold on;
plot(t*1e6, carrier, 'r');             % Carrier
plot(t*1e6, B, 'g');                   % Audio signal
plot(t*1e6, transmitted_signal, 'b');  % Modulated signal
hold off;
legend('Carrier','Audio','Transmitted');
xlabel('Time');
ylabel('Amplitude');
title('Carrier, Audio, and Transmitted Signal');
grid on;

% (2) Frequency domain of transmitted signal
subplot(1,2,2);
plot(f/1e6, abs(X));
xlabel('Frequency (MHz)');
ylabel('|X(f)|');
xlim([95 105]);   % zoom around carrier
title('Transmitted Signal Spectrum');
grid on;
