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
        super().__init__(f"Invalid VNX WWN: {value}")


class EmcVnxWWN(WWN):
    """
    Decoding of VNX WWN (with the contribution of Stanislav M.
    thank you, Stanislav ! :-)
    """

    def __init__(self, address):
        super().__init__(address)

        if self.oui not in '00:60:16':
            raise EmcVnxWWNError('This not a WWN Vnx !')

    def _decode_naa5(self):
        # Decode of VNX/Clariion WWN based on
        # https://prefetch.net/blog/2005/09/26/dissecting-clariion-wwns
        port = int(self.wwn_nodots[7], 16)
        if port >= 8:
            service_processor = 'SPB'
            port -= 8
        else:
            service_processor = 'SPA'

        self._decode = f'VNX/Clariion {service_processor} port {port}'

    def _decode_naa6(self):
        raise NotImplementedError
