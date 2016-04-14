#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .manufacturers.EMC.Symmetrix import EmcVmaxWWN, EmcDmxWWN
from .manufacturers.EMC.Vnx import EmcVnxWWN
from .manufacturers.EMC.Vplex import EmcVplexWWN
from .manufacturers.IBM.NPIV import IbmNpivWWN
from .manufacturers.NetApp.NetApp import NetappFasWWN
from .wwn import WWN, WWNInvalidError

__author__ = 'Julien B. (jbrt)'
__license__ = 'GPLv3'
__version__ = '0.5'
__status__ = 'Production'


class WWNFactoryError(Exception):
    def __init__(self, value):
        super(WWNFactoryError, self).__init__("WWN Factory error: {0!r}".format(value))


class WWNFactory(object):
    """ This class can create objects WWN without knowing the manufacturer from which they come """
    
    _instance = None
    
    def __new__(cls):
        """ Singleton constructor : only one instance of this factory is allowed """

        if not cls._instance:
            cls._instance = super(WWNFactory, cls).__new__(cls)
    
        return cls._instance

    def __init__(self):
        super(WWNFactory, self).__init__()

        self._classes = {'00:00:97': EmcVmaxWWN,
                         '00:60:16': EmcVnxWWN,
                         '00:60:48': EmcDmxWWN,
                         '00:01:44': EmcVplexWWN,
                         '00:a0:98': NetappFasWWN,
                         '0a:98:00': NetappFasWWN,
                         '00:50:76': IbmNpivWWN}

    def create(self, address):
        """ Create a WWN object

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

# EOF
