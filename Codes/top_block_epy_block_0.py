import numpy as np
from gnuradio import gr

class blk(gr.sync_block):

    def __init__(self, N=1024):
        gr.sync_block.__init__(
            self,
            name="corr_for_time_sink",
            in_sig=[np.complex64, np.complex64],
            out_sig=[np.float32]        # stream output for Time Sink
        )

        self.N = N
        self.buf1 = np.zeros(N, dtype=np.complex64)
        self.buf2 = np.zeros(N, dtype=np.complex64)

    def work(self, input_items, output_items):

        x = input_items[0]
        y = input_items[1]

        L = min(len(x), self.N)

        # ---- update circular buffers ----
        self.buf1 = np.roll(self.buf1, -L)
        self.buf2 = np.roll(self.buf2, -L)

        self.buf1[-L:] = x[:L]
        self.buf2[-L:] = y[:L]

        # ---- CROSS CORRELATION ----
        r = np.correlate(self.buf1, self.buf2.conj(), mode='full')

        # magnitude + normalize
        r = np.abs(r)
        if np.max(r) > 0:
            r = r / np.max(r)

        # take center N samples (so Time Sink shows a stable frame)
        mid = len(r) // 2
        r_cut = r[mid - self.N//2 : mid + self.N//2]

        # ---- OUTPUT AS STREAM ----
        out = output_items[0]
        n = min(len(out), len(r_cut))

        out[:n] = r_cut[:n].astype(np.float32)

        # also print estimated delay
        peak = np.argmax(r) - (self.N - 1)
        print("Estimated delay:", peak, "samples")

        return n
