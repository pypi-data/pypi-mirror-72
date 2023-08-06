# Copyright (c) IMToolkit Development Team
# This toolkit is released under the MIT License, see LICENSE.txt

import itertools
import numpy as np
from .Modulator import Modulator

#from numba import jitclass, uint32, complex64
class OSTBCode(object):
    """Orthogonal space-time block code (OSTBC). A seminal research can be found in [1].

    - [1] S. Alamouti, ``A simple transmit diversity technique for wireless communications,'' IEEE J. Sel. Areas Commun., vol. 16, no. 8, pp. 1451--1458, 1998.
    """

    def __init__(self, M, modtype, L, nsymbols=1):
        """
        Args:
            M (int): the number of transmit antennas.
            modtype (string): the constellation type.
            L (int): the constellation size.
            nsymbols (int): the number of embedded symbols.
        """
        self.M = M
        mod = Modulator(modtype, L)

        if M == 2:
            nsymbols = M

        elif M == 4:
            if modtype == "PAM":
                nsymbols = M
            else:
                if nsymbols != 2 and nsymbols != 3:
                    print("Please specify nsymbols = 2 or 3. I use nsymbols = 2.")
                    nsymbols = 2
                if modtype == "QAM":
                    print("Note that the space-time codewords become non-orthogonal.")
        elif M == 8:
            if modtype == "PAM":
                nsymbols = M
            else:
                print("OSTBC with M=8 and PSK is not supported")
        elif M == 16:
            nsymbols = M

        self.B = nsymbols * np.log2(L)
        self.Nc = int(2 ** self.B)

        # initialize codes
        kfoldsymbols = np.array(list(itertools.product(mod.symbols, repeat=nsymbols)))  # L^nsymbols \times nsymbols

        self.codes = np.zeros((self.Nc, M, M), dtype=complex)
        for i in range(kfoldsymbols.shape[0]):
            s = kfoldsymbols[i, :]

            if M == 2:
                self.codes[i] = [[s[0], s[1]], [-np.conj(s[1]), np.conj(s[0])]]
                self.codes[i] /= np.sqrt(nsymbols)

            if M == 4:
                if modtype == "PAM":
                    self.codes[i, 0, 0] = s[0]
                    self.codes[i, 0, 1] = s[1]
                    self.codes[i, 0, 2] = s[2]
                    self.codes[i, 0, 3] = s[3]
                    self.codes[i, 1, 0] = -s[1]
                    self.codes[i, 1, 1] = s[0]
                    self.codes[i, 1, 2] = -s[3]
                    self.codes[i, 1, 3] = s[2]
                    self.codes[i, 2, 0] = -s[2]
                    self.codes[i, 2, 1] = s[3]
                    self.codes[i, 2, 2] = s[0]
                    self.codes[i, 2, 3] = -s[1]
                    self.codes[i, 3, 0] = -s[3]
                    self.codes[i, 3, 1] = -s[2]
                    self.codes[i, 3, 2] = s[1]
                    self.codes[i, 3, 3] = s[0]
                    self.codes[i] /= np.sqrt(nsymbols)
                else:
                    if nsymbols == 2:
                        self.codes[i, 0, 0] = s[0]
                        self.codes[i, 0, 1] = s[1]
                        self.codes[i, 1, 0] = -np.conj(s[1])
                        self.codes[i, 1, 1] = np.conj(s[0])
                        self.codes[i, 2, 2] = s[0]
                        self.codes[i, 2, 3] = s[1]
                        self.codes[i, 3, 2] = -np.conj(s[1])
                        self.codes[i, 3, 3] = np.conj(s[0])
                        self.codes[i] /= np.sqrt(nsymbols)
                    elif nsymbols == 3:
                        self.codes[i, 0, 0] = s[0]
                        self.codes[i, 0, 1] = s[1]
                        self.codes[i, 0, 2] = s[2]
                        self.codes[i, 1, 0] = -np.conj(s[1])
                        self.codes[i, 1, 1] = np.conj(s[0])
                        self.codes[i, 1, 3] = s[2]
                        self.codes[i, 2, 0] = np.conj(s[2])
                        self.codes[i, 2, 2] = -np.conj(s[0])
                        self.codes[i, 2, 3] = s[1]
                        self.codes[i, 3, 1] = np.conj(s[2])
                        self.codes[i, 3, 2] = -np.conj(s[1])
                        self.codes[i, 3, 3] = -s[0]
                        self.codes[i] /= np.sqrt(nsymbols)


            elif M == 8:
                if modtype == "PAM":
                    self.codes[i, 0] = [+s[0], +s[1], +s[2], +s[3], +s[4], +s[5], +s[6], +s[7]]
                    self.codes[i, 1] = [-s[1], +s[0], +s[3], -s[2], +s[5], -s[4], -s[7], +s[6]]
                    self.codes[i, 2] = [-s[2], -s[3], +s[0], +s[1], +s[6], +s[7], -s[4], -s[5]]
                    self.codes[i, 3] = [-s[3], +s[2], -s[1], +s[0], +s[7], -s[6], +s[5], -s[4]]
                    self.codes[i, 4] = [-s[4], -s[5], -s[6], -s[7], +s[0], +s[1], +s[2], +s[3]]
                    self.codes[i, 5] = [-s[5], +s[4], -s[7], +s[6], -s[1], +s[0], -s[3], +s[2]]
                    self.codes[i, 6] = [-s[6], +s[7], +s[4], -s[5], -s[2], +s[3], +s[0], -s[1]]
                    self.codes[i, 7] = [-s[7], -s[6], +s[5], +s[4], -s[3], -s[2], +s[1], +s[0]]
                    self.codes[i] /= np.sqrt(nsymbols)

            elif M == 16:
                for k in range(8):
                    self.codes[i, 0 + k * 2, 0 + k * 2] = s[0 + k * 2]
                    self.codes[i, 0 + k * 2, 1 + k * 2] = s[1 + k * 2]
                    self.codes[i, 1 + k * 2, 0 + k * 2] = -np.conj(s[1 + k * 2])
                    self.codes[i, 1 + k * 2, 1 + k * 2] = np.conj(s[0 + k * 2])
                self.codes[i] /= np.sqrt(2)

    def putRate(self):
        print("B / M = %d / %d = %d [bit/symbol]" % (self.B, self.M, self.B / self.M))
