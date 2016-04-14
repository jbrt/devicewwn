#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from devicewwn.wwn import WWN, WWNInvalidError

__author__ = 'Julien B. (jbrt)'
__license__ = 'GPLv3'
__version__ = '0.5'
__status__ = 'Production'


class EmcVnxWWNError(WWNInvalidError):
    def __init__(self, value):
        super(EmcVnxWWNError, self).__init__("Invalid VNX WWN: {0!r}".format(value))


class EmcVnxWWN(WWN):
    """ Decoding of VNX WWN NOT YET IMPLEMENTED !! """

    def __init__(self, address):
        super(EmcVnxWWN, self).__init__(address)

        if self.oui not in '00:60:16':
            raise EmcVnxWWNError('This not a WWN Vnx !')

    def _decodeNaa5(self):
        raise NotImplementedError

    def _decodeNaa6(self):
        raise NotImplementedError

# EOF
