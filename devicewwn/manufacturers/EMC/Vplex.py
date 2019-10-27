#!/usr/bin/env python3
# coding: utf-8

"""
VPLEX WWN
"""

from devicewwn.wwn import WWN, WWNInvalidError


class EmcVplexWWNError(WWNInvalidError):
    """
    Generic VPLEX Exception
    """
    def __init__(self, value):
        super(EmcVplexWWNError, self).__init__("Invalid VPLEX WWN: {0!r}".
                                               format(value))


class EmcVplexWWN(WWN):
    """
    Decoding of VPLEX WWN (Warning: use this version with VS2
    hardware only !)
    """

    io_module = {'0': 'Frontend',
                 '1': 'Backend',
                 '2': 'WAN-Com',
                 '3': 'Local-Com'}

    def __init__(self, address):
        super(EmcVplexWWN, self).__init__(address)

        if self.oui not in '00:01:44':
            raise EmcVplexWWNError('This not a WWN Vplex !')

    def _decodeNaa5(self):
        seed = self.wwn_nodots[9:14]
        port_type = self.io_module[self.wwn_nodots[14]] if self.wwn_nodots[14] in self.io_module else '(Unknown)'
        port_number = self.wwn_nodots[-1]
        
        self._decode = 'VPLEX Seed:%s IOModule:%s Port:%s' % \
                       (seed, port_type, port_number)
