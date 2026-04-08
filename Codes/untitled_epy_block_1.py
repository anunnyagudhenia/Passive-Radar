import numpy as np
from gnuradio import gr
from scipy.signal import correlate


class blk(gr.sync_block):

    def __init__(self, N=500, fs=1e6):
        gr.sync_block.__init__(
            self,
            name='corr_and_delay',
            in_sig=[np.float32, np.float32],
            out_sig=[np.float32, np.float32]   # 0: corr curve, 1: delay
        )

        self.N = N
        self.fs = fs

        self.b1 = []
        self.b2 = []

        self.corr = np.zeros(2*N-1)
        self.ptr = 0

        self.delay_val = 0


    def work(self, input_items, output_items):

        ch1 = input_items[0]
        ch2 = input_items[1]

        out_corr  = output_items[0]
        out_delay = output_items[1]

        # ---- stream correlation ----
        for i in range(len(out_corr)):
            if self.ptr < len(self.corr):
                out_corr[i] = self.corr[self.ptr]
                self.ptr += 1
            else:
                out_corr[i] = 0

        # ---- stream delay as constant ----
        out_delay[:] = self.delay_val


        # ---- collect ----
        self.b1.extend(ch1.tolist())
        self.b2.extend(ch2.tolist())


        if len(self.b1) >= self.N:

            x = np.array(self.b1[:self.N])
            y = np.array(self.b2[:self.N])

            # ===== TRUE CORRELATION =====
            r = correlate(x-np.mean(x), y-np.mean(y), 'full')
            self.corr = r
            self.ptr = 0

            # ---- DELAY ESTIMATE ----
            lag_index = np.argmax(np.abs(r))
            delay_samples = lag_index - (self.N-1)

            self.delay_val = delay_samples / self.fs * 1e6

            self.b1 = []
            self.b2 = []

        return len(out_corr)
