#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from devicewwn.wwn import WWN, WWNInvalidError

__author__ = 'Julien B. (jbrt)'
__license__ = 'GPLv3'
__version__ = '0.5'
__status__ = 'Production'


class IbmNpivWWNError(WWNInvalidError):
    def __init__(self, value):
        super(IbmNpivWWNError, self).__init__("Invalid IBM WWN: {0!r}".format(value))


class IbmNpivWWN(WWN):

    def __init__(self, address):
        super(IbmNpivWWN, self).__init__(address)

        if not self.oui == '00:50:76':
            raise IbmNpivWWNError('This not a IBM NPIV WWN !')

    def _decodeNaa5(self):
        raise NotImplementedError

    def _decodeNaa6(self):
        raise NotImplementedError

# EOF
