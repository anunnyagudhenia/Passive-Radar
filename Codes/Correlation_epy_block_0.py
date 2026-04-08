import numpy as np
from gnuradio import gr
import matplotlib.pyplot as plt

class blk(gr.sync_block):
    def __init__(self, vec_len=2048, delay_samples=200):
        gr.sync_block.__init__(
            self,
            name="python_corr_plot",
            in_sig=[np.complex64],
            out_sig=[]
        )

        self.N = vec_len
        self.delay = delay_samples

        # Matplotlib setup
        plt.ion()
        self.fig, self.ax = plt.subplots()
        self.line, = self.ax.plot(np.zeros(2*self.N-1))
        self.ax.set_title("Cross-Correlation")
        self.ax.set_xlabel("Lag (samples)")
        self.ax.set_ylabel("Magnitude")

        # buffer for accumulating samples
        self.buffer = np.zeros(self.N, dtype=np.complex64)
        self.index = 0

    def work(self, input_items, output_items):
        inp = input_items[0]

        # how many samples needed to fill buffer
        needed = self.N - self.index

        if len(inp) < needed:
            self.buffer[self.index:self.index+len(inp)] = inp
            self.index += len(inp)
            return len(inp)

        # fill remaining buffer
        self.buffer[self.index:] = inp[:needed]
        self.index = 0

        # signals
        direct = self.buffer
        delayed = np.roll(self.buffer, self.delay)

        # correlation
        corr = np.abs(np.correlate(direct, delayed, mode="full"))

        # update plot
        self.line.set_ydata(corr)
        self.ax.relim()
        self.ax.autoscale_view()
        plt.pause(0.001)

        return needed
