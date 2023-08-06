# Copyright (c) IMToolkit Development Team
# This toolkit is released under the MIT License, see LICENSE.txt

import os
from tqdm import tqdm, trange

if os.getenv("USECUPY") == "1":
    from cupy import *
else:
    from numpy import *

from .Simulator import Simulator
from .Util import getXORtoErrorBitsArray, inv_dB, randn_c


class SemiUnitaryDifferentialMLDSimulator(Simulator):
    """A simulator that relies on the non-coherent maximum likelihood detector, where semi-unitary matrices are used for differential encoding and decdoing. The semi-unitary matrix is defined by $U U^H = \alpha I_M$ and $\alpha \in \mathbb{R}$. The environment variable USECUPY determines whether to use cupy or not."""

    def __init__(self, codes, channel):
        """
        Args:
            codes (ndarray): an input codebook, which is generated on the CPU memory and is transferred into the GPU memory.
            channel (imtoolkit.Channel): a channel model used in simulation.
        """
        super().__init__(codes, channel)

    def simulateBERReference(self, params, outputFile=True, printValue=True):
        """Simulates BER values at multiple SNRs, where the straightforward reference algorithm is used. Note that this time complexity is unrealistically high. 

        Args:
            params (imtoolkit.Parameter): simulation parameters.
            outputFile (bool): a flag that determines whether to output the obtained results to the results/ directory.
            printValue (bool): a flag that determines whether to print the simulated values.

        Returns:
            ret (dict): a dict that has two keys: snr_dB and ber, and contains the corresponding results. All the results are transferred into the CPU memory.
        """

        IT, M, N, Nc, B, codes = params.IT, params.M, params.N, self.Nc, self.B, self.codes
        snr_dBs = linspace(params.snrfrom, params.to, params.len)
        sigmav2s = 1.0 / inv_dB(snr_dBs)
        xor2ebits = getXORtoErrorBitsArray(Nc)

        bers = zeros(len(snr_dBs))
        for i in trange(len(snr_dBs)):
            errorBits = 0
            v0 = randn_c(N, M) * sqrt(sigmav2s[i])  # N \times M
            s0 = eye(M, dtype=complex)
            rs0 = s0  # the estimated codeword at the receiver
            currentBeta = linalg.norm(rs0)  # the estimated normalizing factor at the receiver
            for _ in range(IT):
                codei = random.randint(0, Nc)
                s1 = matmul(s0, codes[codei]) / linalg.norm(s0)  # semi-unitary differential encoding

                self.channel.randomize()
                h = self.channel.getChannel()  # N \times M
                v1 = randn_c(N, M) * sqrt(sigmav2s[i])  # N \times M

                y0 = matmul(h, s0) + v0  # N \times M
                y1 = matmul(h, s1) + v1  # N \times M

                # semi-unitary non-coherent detection
                p = square(abs(y1 - matmul(y0, codes) / currentBeta))  # Nc \times N \times M
                norms = sum(p, axis=(1, 2))  # summation over the (N,M) axes
                mini = argmin(norms)
                errorBits += sum(xor2ebits[codei ^ mini])

                rs1 = matmul(rs0, codes[mini]) / currentBeta
                currentBeta = linalg.norm(rs1)
                v0 = v1
                s0 = s1
                rs0 = rs1

            bers[i] = errorBits / (IT * B)
            if printValue:
                print("At SNR = %1.2f dB, BER = %d / %d = %1.10e" % (snr_dBs[i], errorBits, IT * B, bers[i]))

        ret = self.dicToNumpy({"snr_dB": snr_dBs, "ber": bers})
        if outputFile:
            self.saveCSV(params.arg, ret)
            print(ret)
        return ret

    def simulateBERParallel(self, params, outputFile=True, printValue=True):
        """Simulates BER values at multiple SNRs, where the massively parallel algorithm is used. This implementation is especially designed for cupy.

        Args:
            params (imtoolkit.Parameter): simulation parameters.
            outputFile (bool): a flag that determines whether to output the obtained results to the results/ directory.
            printValue (bool): a flag that determines whether to print the simulated values.

        Returns:
            ret (dict): a dict that has two keys: snr_dB and ber, and contains the corresponding results. All the results are transferred into the CPU memory.
        """

        M, N, ITo, ITi, Nc, B, codes = params.M, params.N, params.ITo, params.ITi, self.Nc, self.B, self.codes

        if Nc > ITi:
            print("ITi should be larger than Nc = %d." % Nc)

        snr_dBs = linspace(params.snrfrom, params.to, params.len)
        lsnr = len(snr_dBs)
        sigmav2s = 1.0 / inv_dB(snr_dBs)
        xor2ebits = getXORtoErrorBitsArray(Nc)
        codesmat = hstack(codes)  # M \times M * Nc
        eyes = tile(eye(M, dtype=complex), lsnr * ITi).T.reshape(lsnr, ITi, M, M)  # lsnr \times ITi \times M \times M

        indspermute = random.permutation(arange(ITi))
        codei = tile(arange(Nc), int(ceil(ITi / Nc)))[0:ITi]
        x1 = take(codes, codei, axis=0)  # ITi \times M \times M very slow
        v0 = randn_c(ITi, N, M)  # ITi \times N \times M
        s0 = eyes[0]  # ITi \times M \times M
        rs0 = eyes  # the estimated codeword at the receiver
        rs1 = zeros((lsnr, ITi, M, M), dtype=complex)  # lsnr \times ITi \times M \times M
        currentBetas = repeat(sqrt(M), lsnr * ITi).reshape(lsnr, ITi, 1,
                                                           1)  # the estimated normalizing factor at the receiver, which corresponds to each SNR

        bers = zeros(lsnr)
        for ito in trange(ITo):
            self.channel.randomize()
            h = self.channel.getChannel().reshape(ITi, N, M)  # ITi \times N \times M
            v1 = randn_c(ITi, N, M)  # ITi \times N \times M
            # semi-unitary differential encoding
            s1 = matmul(s0, x1) / linalg.norm(s0, axis=(1, 2)).reshape(ITi, 1, 1)  # ITi \times M \times M

            for i in range(lsnr):
                y0 = matmul(h, s0) + v0 * sqrt(sigmav2s[i])  # ITi \times N \times M
                y1 = matmul(h, s1) + v1 * sqrt(sigmav2s[i])  # ITi \times N \times M
                y0x = matmul(y0, codesmat) / currentBetas[i]  # ITi \times N \times M * Nc

                ydiff = tile(y1, Nc) - y0x  # ITi \times N \times M * Nc
                ydifffro = square(abs(ydiff)).reshape(ITi, N, Nc, M)  # ITi \times N \times Nc \times M
                norms = sum(ydifffro, axis=(1, 3))  # ITi \times Nc
                mini = argmin(norms, axis=1)  # ITi

                rs1[i] = matmul(rs0[i], codes[mini]) / currentBetas[i]
                currentBetas[i] = linalg.norm(rs1[i], axis=(1, 2)).reshape(ITi, 1, 1)

                errorBits = sum(xor2ebits[codei ^ mini])
                bers[i] += errorBits

                if printValue:
                    nbits = (ito + 1) * ITi * B
                    print("At SNR = %1.2f dB, BER = %d / %d = %1.10e" % (snr_dBs[i], bers[i], nbits, bers[i] / nbits))

            v0 = v1
            s0 = s1
            rs0 = rs1
            codei = codei[indspermute]
            x1 = x1[indspermute]

        bers /= ITo * ITi * B
        ret = self.dicToNumpy({"snr_dB": snr_dBs, "ber": bers})
        if outputFile:
            self.saveCSV(params.arg, ret)
            print(ret)
        return ret
