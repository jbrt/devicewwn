#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
IBM WWN
"""

from devicewwn.wwn import WWN, WWNInvalidError


class IbmNpivWWNError(WWNInvalidError):
    """
    Generic IBM Exception
    """
    def __init__(self, value):
        super(IbmNpivWWNError, self).__init__("Invalid IBM WWN: {0!r}".
                                              format(value))


class IbmNpivWWN(WWN):
    """
    Class for handling IBM WWN
    """

    def __init__(self, address):
        super(IbmNpivWWN, self).__init__(address)

        if not self.oui == '00:50:76':
            raise IbmNpivWWNError('This not a IBM NPIV WWN !')

    def _decodeNaa5(self):
        raise NotImplementedError

    def _decodeNaa6(self):
        raise NotImplementedError
