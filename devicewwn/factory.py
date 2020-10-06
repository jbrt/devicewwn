# coding: utf-8

"""
Factory pattern used for building the right WWN object
"""

from devicewwn.manufacturers.emc.symmetrix import EmcVmaxWWN, EmcDmxWWN
from devicewwn.manufacturers.emc.vnx import EmcVnxWWN
from devicewwn.manufacturers.emc.vplex import EmcVplexWWN
from devicewwn.manufacturers.ibm.npiv import IbmNpivWWN
from devicewwn.manufacturers.netapp.netapp import NetappFasWWN
from devicewwn.manufacturers.hitachi.hitachi import HitachiWWN
from devicewwn.wwn import WWN, WWNInvalidError


class WWNFactoryError(Exception):
    """
    Generic Factory Exception
    """
    def __init__(self, value):
        super().__init__(f"WWN Factory error: {value}")


class WWNFactory:
    """
    This class can create objects WWN without knowing the manufacturer
    from which they come
    """
    _instance = None

    def __new__(cls):
        """
        Singleton constructor : only one instance of this factory is
        allowed
        """

        if not cls._instance:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self):
        super().__init__()

        self._classes = {'00:00:97': EmcVmaxWWN,
                         '00:60:16': EmcVnxWWN,
                         '00:60:48': EmcDmxWWN,
                         '00:01:44': EmcVplexWWN,
                         '00:a0:98': NetappFasWWN,
                         '0a:98:00': NetappFasWWN,
                         '00:50:76': IbmNpivWWN,
                         '00:60:e8': HitachiWWN}

    def create(self, address: str) -> WWN:
        """
        Create a WWN object
        :param address: String to convert
        :type address: str
        :except WWNFactoryError
        """
        try:
            new_wwn = WWN(address)
        except WWNInvalidError:
            raise WWNFactoryError

        if new_wwn.oui in self._classes:
            wwn_created = self._classes[new_wwn.oui](new_wwn.wwn)
            del new_wwn
        else:
            wwn_created = new_wwn

        return wwn_created
