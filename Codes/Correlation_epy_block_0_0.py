import numpy as np
from gnuradio import gr

class blk(gr.sync_block):
    """Streaming cross-correlation: y[n] * conj(x[n])"""

    def __init__(self, example_param=1):
        gr.sync_block.__init__(
            self,
            name='Streaming XCorr',
            in_sig=[np.complex64, np.complex64],   # 2 stream inputs
            out_sig=[np.complex64]                  # 1 stream output
        )

    def work(self, input_items, output_items):
        x = input_items[0]      # reference stream
        y = input_items[1]      # delayed stream

        # streaming cross-correlation (pointwise)
        output_items[0][:] = y * np.conj(x)

        return len(output_items[0])
