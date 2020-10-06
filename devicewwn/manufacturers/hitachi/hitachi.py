# coding: utf-8

"""
Hitachi WWN
"""

from devicewwn.wwn import WWN, WWNInvalidError


class HitachiWWNError(WWNInvalidError):
    """
    Generic Hitachi Exception
    """
    def __init__(self, value):
        super().__init__(f"Invalid Hitachi WWN: {value}")


class HitachiWWN(WWN):
    """
    Decode WWN from Hitachi
    """

    def __init__(self, address):
        super().__init__(address)
        if self.oui != '00:60:e8':
            raise HitachiWWNError('This not a Hitachi !')

    def _decode_naa6(self):
        serial = str(int(self.wwn_nodots[10:14], 16))
        model = 'Hitachi'
        hve = self.wwn[-5:]
        self._decode = f'{model} S/N:{serial} HVE:{hve}'
