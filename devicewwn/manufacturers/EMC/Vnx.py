#!/usr/bin/env python3
# coding: utf-8

"""
VNX WWN
"""

from devicewwn.wwn import WWN, WWNInvalidError


class EmcVnxWWNError(WWNInvalidError):
    """
    Generic VNX Exception
    """
    def __init__(self, value):
        super(EmcVnxWWNError, self).__init__("Invalid VNX WWN: {0!r}".
                                             format(value))


class EmcVnxWWN(WWN):
    """
    Decoding of VNX WWN (with the contribution of Stanislav M.
    thank you, Stanislav ! :-)
    """

    def __init__(self, address):
        super(EmcVnxWWN, self).__init__(address)

        if self.oui not in '00:60:16':
            raise EmcVnxWWNError('This not a WWN Vnx !')

    def _decodeNaa5(self):
        # Decode of VNX/Clariion WWN based on
        # https://prefetch.net/blog/2005/09/26/dissecting-clariion-wwns
        port = int(self.wwn_nodots[7], 16)
        if port >= 8:
            sp = 'SPB'
            port -= 8
        else:
            sp = 'SPA'

        self._decode = 'VNX/Clariion %s port %d' % (sp, port)

    def _decodeNaa6(self):
        raise NotImplementedError
