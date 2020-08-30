# coding: utf-8

"""
IBM WWN
"""

from devicewwn.wwn import WWN, WWNInvalidError


class IbmNpivWWNError(WWNInvalidError):
    """
    Generic ibm Exception
    """
    def __init__(self, value):
        super().__init__(f"Invalid ibm WWN: {value}")


class IbmNpivWWN(WWN):
    """
    Class for handling ibm WWN
    """

    def __init__(self, address):
        super().__init__(address)

        if self.oui != '00:50:76':
            raise IbmNpivWWNError('This not a ibm NPIV WWN !')

    def _decode_naa5(self):
        raise NotImplementedError

    def _decode_naa6(self):
        raise NotImplementedError
