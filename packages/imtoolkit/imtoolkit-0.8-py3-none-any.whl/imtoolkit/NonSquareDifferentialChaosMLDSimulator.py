# Copyright (c) IMToolkit Development Team
# This toolkit is released under the MIT License, see LICENSE.txt

import os
from tqdm import trange
if os.getenv("USECUPY") == "1":
    from cupy import *
else:
    from numpy import *
from .Simulator import Simulator
from .Util import getXORtoErrorBitsArray, inv_dB, randn_c, asnumpy, getDFTMatrix
from .Basis import Basis
from .ChaosBasis import ChaosBasis

class NonSquareDifferentialChaosMLDSimulator(Simulator):
    """A nonsquare differential coding simulator that relies on the chaos-based time-varying unitary concept of [1]. This implementation uses the square-to-nonsquare projection concept of [2] and the adaptive forgetting factor of [3]. The environment variable USECUPY determines whether to use cupy or not.

    - [1] N. Ishikawa and J. Hamamreh, "?????," ????.
    - [2] N. Ishikawa, R. Rajashekar, C. Xu, S. Sugiura, and L. Hanzo, "Differential space-time coding dispensing with channel-estimation approaches the performance of its coherent counterpart in the open-loop massive MIMO-OFDM downlink," IEEE Trans. Commun., vol. 66, no. 12, pp. 6190--6204, 2018.
    - [3] N. Ishikawa, R. Rajashekar, C. Xu, M. El-Hajjar, S. Sugiura, L. L. Yang, and L. Hanzo, "Differential-detection aided large-scale generalized spatial modulation is capable of operating in high-mobility millimeter-wave channels," IEEE J. Sel. Top. Signal Process., in press.
    """

    def __init__(self, codes, channel, txbases, rxbases):
        """
        Args:
            codes (ndarray): an input codebook, which is generated on the CPU memory and is transferred into the GPU memory.
            channel (imtoolkit.Channel): a channel model used in simulation.
            bases (imtoolkit.Basis): a set of bases that projects a unitary matrix on a nonsquare matrix.
        """
        super().__init__(codes, channel)
        self.txbases = self.toXpArray(txbases)
        self.rxbases = self.toXpArray(rxbases)

    def simulateBERReference(self, params, outputFile=True, printValue=True):
        """Simulates BER values at multiple SNRs, where the straightforward reference algorithm is used. Note that this time complexity is very high. Most of this implementation is copied from imtoolkit.NonSquareDifferentialMLDSimulator.

        Args:
            params (imtoolkit.Parameter): simulation parameters.
            outputFile (bool): a flag that determines whether to output the obtained results to the results/ directory.
            printValue (bool): a flag that determines whether to print the simulated values.

        Returns:
            ret (dict): a dict that has two keys: snr_dB and ber, and contains the corresponding results. All the results are transferred into the CPU memory.
        """

        IT, M, N, T, W, Nc, B, codes = params.IT, params.M, params.N, params.T, params.W, self.Nc, self.B, self.codes
        WT, MT = int(W / T), int(M / T)
        txbases, rxbases = self.txbases, self.rxbases
        snr_dBs = linspace(params.snrfrom, params.to, params.len)
        sigmav2s = 1.0 / inv_dB(snr_dBs)
        xor2ebits = getXORtoErrorBitsArray(Nc)

        bers = zeros(len(snr_dBs))
        for i in trange(len(snr_dBs)):
            errorBits = 0

            if params.option == "evex":
                # estimate the initial condition and construct rxbases
                x0 = self.estimateInitialCondition(snr_dBs[i], params)
                E1 = Basis.getGSPE1(params) if params.basis[0] == "g" else None
                rxbases = ChaosBasis(params.basis, params.M, params.T, params.W, x0, params.Ns, E1=E1).bases

            for it in range(IT):
                S0 = eye(M, dtype=complex)
                Yhat0 = Yhat1 = zeros((N, M), dtype=complex)

                self.channel.randomize()
                H = self.channel.getChannel()  # N \times M

                for wi in range(1, WT + 1):
                    if wi <= MT:
                        S1 = eye(M, dtype=complex)
                        Sr1 = txbases[MT - 1, wi - 1]
                        X1 = S1
                        Y1 = matmul(H, Sr1) + randn_c(N, T) * sqrt(sigmav2s[i])  # N \times T
                        Yhat1 += matmul(Y1, rxbases[MT - 1, wi - 1].T.conj())
                    else:
                        txE1 = txbases[wi - 1, 0]  # M \times T
                        rxE1 = rxbases[wi - 1, 0]  # M \times T
                        rxE1H = rxE1.T.conj()
                        Xrs = matmul(codes, rxE1)  # Nc \times M \times T

                        codei = random.randint(0, Nc)
                        X1 = codes[codei]
                        S1 = matmul(S0, X1)
                        Sr1 = matmul(S1, txE1)
                        Y1 = matmul(H, Sr1) + randn_c(N, T) * sqrt(sigmav2s[i])  # N \times T

                        # estimate
                        p = square(abs(Y1 - matmul(Yhat0, Xrs)))  # Nc \times N \times M
                        norms = sum(p, axis=(1, 2))  # summation over the (N,M) axes
                        mini = argmin(norms)
                        Xhat1 = codes[mini]

                        # adaptive forgetting factor
                        Yhd = matmul(Yhat0, Xhat1)
                        D1 = Y1 - matmul(Yhd, rxE1)
                        n1 = square(linalg.norm(D1))
                        estimatedAlpha = N * T * sigmav2s[i] / n1
                        estimatedAlpha = min(max(estimatedAlpha, 0.01), 0.99)
                        Yhat1 = (1.0 - estimatedAlpha) * matmul(D1, rxE1H) + Yhd

                        errorBits += sum(xor2ebits[codei ^ mini])

                    S0 = S1
                    Yhat0 = Yhat1

            bers[i] = errorBits / (IT * B * (W - M)) * T

            if printValue:
                print("At SNR = %1.2f dB, BER = %d / %d = %1.20e" % (
                snr_dBs[i], errorBits, (IT * B * (W - M)) / T, bers[i]))

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

        ITo, ITi, M, N, T, W, Nc, B, codes = params.ITo, params.ITi, params.M, params.N, params.T, params.W, self.Nc, self.B, self.codes
        WT, MT = int(W / T), int(M / T)
        txbases, rxbases = self.txbases, self.rxbases

        if Nc > ITi:
            print("ITi should be larger than Nc = %d." % Nc)

        snr_dBs = linspace(params.snrfrom, params.to, params.len)
        lsnr = len(snr_dBs)
        sigmav2s = 1.0 / inv_dB(snr_dBs)
        xor2ebits = getXORtoErrorBitsArray(Nc)
        eyes = tile(eye(M, dtype=complex), lsnr * ITi).T.reshape(lsnr, ITi, M, M)  # lsnr \times ITi \times M \times M

        # E1 = bases[0]  # M \times T
        # E1H = E1.T.conj()
        # Xrs = matmul(codes, E1)  # Nc \times M \times T
        # Xrsmat = hstack(Xrs)  # M \times T * Nc

        indspermute = random.permutation(arange(ITi))
        codei = tile(arange(Nc), int(ceil(ITi / Nc)))[0:ITi]
        X1 = take(codes, codei, axis=0)  # ITi \times M \times M

        bers = zeros(lsnr)
        for ito in trange(ITo, disable=not printValue):
            self.channel.randomize()
            Ho = self.channel.getChannel().reshape(ITi, N, M)  # ITi \times N \times M
            # The followings are very slow
            # H = asarray(split(tile(Ho, lsnr), lsnr, axis=2)) # lsnr \times ITi \times N \times M
            # H = rollaxis(repeat(Ho, lsnr, axis=0).reshape(ITi, lsnr, N, M), 1) # lsnr \times ITi \times N \times M
            # This simple for loop is the fastest
            H = zeros((lsnr, ITi, N, M), dtype=complex)
            for i in range(lsnr):
                H[i] = Ho

            S0 = eyes[0]  # ITi \times M \times M
            Yhat0 = Yhat1 = zeros((lsnr, ITi, N, M), dtype=complex)  # lsnr \times ITi \times N \times M

            for wi in range(1, WT + 1):
                Vo = randn_c(ITi, N, T)  # ITi \times N \times T
                V1 = zeros((lsnr, ITi, N, T), dtype=complex)
                for i in range(lsnr):
                    V1[i] = sqrt(sigmav2s[i]) * Vo

                if wi <= MT:
                    S1 = eyes[0]
                    Y1 = matmul(H, txbases[MT - 1, wi - 1]) + V1  # lsnr \tiems ITi \times N \times T
                    Yhat1 += matmul(Y1, rxbases[MT - 1, wi - 1].T.conj())  # lsnr \tiems ITi \times N \times M
                else:
                    txE1 = txbases[wi - 1, 0]  # M \times T
                    rxE1 = rxbases[wi - 1, 0]  # M \times T
                    rxE1H = rxE1.T.conj()
                    Xrs = matmul(codes, rxE1)  # Nc \times M \times T
                    Xrsmat = hstack(Xrs)  # M \times T * Nc

                    codei = codei[indspermute]
                    X1 = X1[indspermute]  # ITi \times M \times M
                    S1 = matmul(S0, X1)  # ITi \times M \times M
                    Sr1 = matmul(S1, txE1)  # ITi \times M \times T
                    Y1 = matmul(H, Sr1) + V1  # lsnr \times ITi \times N \times T

                    # estimate
                    YhXrs = matmul(Yhat0, Xrsmat)  # lsnr \times ITi \times N \times T * Nc
                    ydifffro = square(abs(Y1 - YhXrs)).reshape(lsnr, ITi, N, Nc, T)
                    norms = sum(ydifffro, axis=(2, 4))  # lsnr \times ITi \times Nc
                    mini = argmin(norms, axis=2)  # lsnr \times ITi
                    Xhat1 = codes[mini]  # lsnr \times ITI \times M \time M

                    # adaptive forgetting factor
                    Yhd = matmul(Yhat0, Xhat1)  # lsnr \times ITi \times N \times M
                    D1 = Y1 - matmul(Yhd, rxE1)  # lsnr \times ITi \times N \times T
                    n1 = sum(square(abs(D1)), axis=(2, 3))  # lsnr \times ITi

                    elphas = N * T * matmul(diag(sigmav2s), 1.0 / n1)  # lsnr \times ITi estimated alpha coefficients
                    elphas[where(elphas < 0.01)] = 0.01
                    elphas[where(elphas > 0.99)] = 0.99

                    elphastensor = repeat(1 - elphas, N * M).reshape(lsnr, ITi, N, M)
                    Yhat1 = elphastensor * matmul(D1, rxE1H) + Yhd  # lsnr \times ITi \times N \times M
                    bers += sum(xor2ebits[codei ^ mini], axis=1)  # lsnr

                S0 = S1
                Yhat0 = Yhat1

            if printValue:
                nbits = (ito + 1) * ITi * B * (W - M) / T
                for i in range(lsnr):
                    print("At SNR = %1.2f dB, BER = %d / %d = %1.10e" % (
                        snr_dBs[i], bers[i], nbits, bers[i] / nbits))

        bers = bers / (ITo * ITi * B * (W - M)) * T
        ret = self.dicToNumpy({"snr_dB": snr_dBs, "ber": bers})
        if outputFile:
            self.saveCSV(params.arg, ret)
            print(ret)
        return ret


    def estimateInitialCondition(self, snr_dB, params):
        """Eve estimates the initial condition x_0 of the ChaosBasis.py

        Args:
            snr_dB (float):
            params (imtoolkit.Parameter): simulation parameters.

        Returns:
            ret (float): the estimated initial condition of the logistic map.
        """

        IT, M, N, T, W, Nc, B, codes = params.IT, params.M, params.N, params.T, params.W, self.Nc, self.B, self.codes
        WT, MT = int(W / T), int(M / T)
        txbases = self.txbases
        sigmav2 = 1.0 / inv_dB(snr_dB)

        tE = txbases[0]
        print("True E(M/T) = " + str(tE))

        S0 = eye(M, dtype=complex)
        Yhat0 = Yhat1 = zeros((N, M), dtype=complex)

        self.channel.randomize()
        H = self.channel.getChannel()  # N \times M
        Y = matmul(H, tE) + randn_c(N, M) * sqrt(sigmav2)  # N \times M

        # Chaos DFT basis
        DFT = getDFTMatrix(M)
        xu = 2.0 * arcsin(sqrt(params.x0)) / pi
        print(exp(2.j * pi * xu) * DFT) # == tE
        HW = matmul(H, DFT)
        print(Y -  HW * exp(2.j * pi * xu)) # 真値x0ならノルムがゼロになる
        return params.x0

