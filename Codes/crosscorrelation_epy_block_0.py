import numpy as np
from gnuradio import gr

class blk(gr.basic_block):
    """
    Cross-correlation block for passive radar.
    Input 0 : reference vector (complex)
    Input 1 : surveillance vector (complex)
    Output  : cross-correlation magnitude (float)
    """

    def __init__(self, N=4096):
        gr.basic_block.__init__(
            self,
            name="cross_corr_block",
            in_sig=[(np.complex64, N), (np.complex64, N)],
            out_sig=[(np.float32, N)],
        )
        self.N = N

    def general_work(self, input_items, output_items):
        ref = input_items[0][0]          # reference vector
        surv = input_items[1][0]         # surveillance vector
        out  = output_items[0][0]

        # Remove DC
        ref  = ref  - np.mean(ref)
        surv = surv - np.mean(surv)

        # FFT
        REF  = np.fft.fft(ref)
        SURV = np.fft.fft(surv)

        # Cross-correlation via frequency domain
        R = np.fft.ifft( SURV * np.conj(REF) )

        # Shift lag zero to center
        R = np.fft.fftshift(R)

        # Magnitude (real output)
        R_mag = np.abs(R)

        # Normalize
        R_mag = R_mag / (np.max(R_mag) + 1e-12)

        # Output
        out[:] = R_mag.astype(np.float32)

        # Consume 1 vector from each input
        self.consume(0, 1)
        self.consume(1, 1)

        return 1
