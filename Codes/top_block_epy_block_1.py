import numpy as np
from gnuradio import gr

class blk(gr.sync_block):

    def __init__(self, N=1024):
        gr.sync_block.__init__(
            self,
            name="cross_corr",
            in_sig=[np.complex64, np.complex64],
            out_sig=[np.float32]        # ← CORRECT TYPE
        )

        self.N = N
        self.buf1 = np.zeros(N, dtype=np.complex64)
        self.buf2 = np.zeros(N, dtype=np.complex64)

    def work(self, input_items, output_items):

        x = input_items[0]
        y = input_items[1]

        L = min(len(x), self.N)

        # shift buffers
        self.buf1 = np.roll(self.buf1, -L)
        self.buf2 = np.roll(self.buf2, -L)

        self.buf1[-L:] = x[:L]
        self.buf2[-L:] = y[:L]

        # CROSS correlation
        r = np.correlate(self.buf1, self.buf2.conj(), mode='full')

        r = np.abs(r)

        # 👉 ESTIMATED DELAY INDEX
        delay_index = np.argmax(r)

        # 👉 normalized peak value
        peak = r[delay_index] / (np.max(r) + 1e-12)

        out = output_items[0]

        # write SAME number of output samples as input
        out[:] = peak

        return len(out)
