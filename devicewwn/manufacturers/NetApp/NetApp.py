#!/usr/bin/env python3
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
        super(NetappFasWWNError, self).__init__("Invalid NetApp WWN: {0!r}".
                                                format(value))


class NetappFasWWN(WWN):
    """
    Generic class for handling NetApp WWN
    """

    def __init__(self, address):
        super(NetappFasWWN, self).__init__(address)

        if self.oui not in ('00:a0:98', '0a:98:00'):
            raise NetappFasWWNError('This not a WWN NetApp !')

    def _decodeNaa6(self):
        mode = ''
        serial = str(binascii.unhexlify(self.wwn_nodots[8:]), 'UTF-8')

        if self.oui == '00:a0:98':
            mode = 'C-Mode'

        if self.oui == '0a:98:00':
            mode = '7-Mode'
        
        self._decode = 'NetApp %s LUN Serial#:%s' % (mode, serial)
