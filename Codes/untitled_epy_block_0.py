import numpy as np
from gnuradio import gr

class blk(gr.basic_block):
    """
    Input:  complex stream
    Output: complex stream (normalized autocorrelation samples)
    """

    def __init__(self):
        gr.basic_block.__init__(
            self,
            name="autocorr_stream_final",
            in_sig=[np.complex64],
            out_sig=[np.complex64],
        )

        self.N = 4096
        self.buf = np.zeros(self.N, dtype=np.complex64)
        self.idx = 0


    def general_work(self, input_items, output_items):
        x   = input_items[0]
        out = output_items[0]

        ni = len(x)
        no = len(out)
        produced = 0

        # Fill buffer
        for i in range(ni):
            self.buf[self.idx] = x[i]
            self.idx += 1

            # Buffer full → compute autocorrelation
            if self.idx == self.N:

                # --- PRE-PROCESS BUFFER ---
                buf = self.buf.copy()

                # Remove DC offset
                buf = buf - np.mean(buf)

                # Apply Hanning window
                buf = buf * np.hanning(self.N)

                # --- AUTOCORRELATION ---
                X = np.fft.fft(buf)
                R = np.fft.ifft(X * np.conj(X))

                # Shift peak to center
                R = np.fft.fftshift(R)

                # Normalize amplitude to 1
                R = R / (np.max(np.abs(R)) + 1e-12)

                # Store for streaming
                self.current = R.astype(np.complex64)
                self.current_idx = 0
                self.idx = 0


        # Stream out autocorrelation result
        if hasattr(self, 'current'):
            remaining = len(self.current) - self.current_idx
            to_output = min(remaining, no)

            out[:to_output] = self.current[self.current_idx:self.current_idx+to_output]
            self.current_idx += to_output
            produced = to_output

            # Finished streaming the vector
            if self.current_idx >= len(self.current):
                del self.current
                del self.current_idx

        # Consume input
        self.consume(0, ni)

        return produced
