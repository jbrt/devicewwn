# coding: utf-8

"""
NetApp WWN
"""

import binascii
from devicewwn.wwn import WWN, WWNInvalidError


class NetappFasWWNError(WWNInvalidError):
    """
    Generic NetAPP Exception
    """
    def __init__(self, value):
        super().__init__(f"Invalid netapp WWN: {value}")


class NetappFasWWN(WWN):
    """
    Generic class for handling netapp WWN
    """

    def __init__(self, address):
        super().__init__(address)

        if self.oui not in ('00:a0:98', '0a:98:00'):
            raise NetappFasWWNError('This not a WWN netapp !')

    def _decode_naa5(self):
        raise NotImplementedError

    def _decode_naa6(self):
        mode = ''
        serial = str(binascii.unhexlify(self.wwn_nodots[8:]), 'UTF-8')

        if self.oui == '00:a0:98':
            mode = 'C-Mode'

        if self.oui == '0a:98:00':
            mode = '7-Mode'

        self._decode = f'netapp {mode} LUN Serial#:{serial}'
