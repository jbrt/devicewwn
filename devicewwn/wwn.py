# coding: utf-8

"""
WWN object used for manipulating and comparing WWN addresses
"""

import abc
import re


class WWNInvalidError(ValueError):
    """
    Generic WWN Exception
    """
    def __init__(self, value):
        super().__init__(f"Invalid FC address: {value}")


class WWN:
    """
    Main class of the package - create WWN object
    """

    def __init__(self, address: str):
        """
        Constructor
        :param address: String representing a WWN object (with ':' or not)
        :type address: str
        :except WWNInvalidError:
        """
        super().__init__()
        self._address = address.wwn if isinstance(address, WWN) else self._normalize(address)
        self._decode = ''

        if self._address[0] == '5':
            self._decode_naa5()

        if self._address[0] == '6':
            self._decode_naa6()

    @classmethod
    def _normalize(cls, address: str):
        """
        Class method used for normalize a WWN
        :param address: String to normalize (contains ':' or not)
        :type address: str
        :except WWNInvalidError:
        """
        regexps = [re.compile("^([0-9a-fA-F]{16})$"),
                   re.compile("^([0-9a-fA-F]{32})$"),
                   re.compile("^([0-9a-fA-F]{2}|:){15}$"),
                   re.compile("^([0-9a-fA-F]{2}|:){31}$")]

        if not any(one_regexp.match(address) for one_regexp in regexps):
            raise WWNInvalidError(address)

        cls._address = address if ':' in address else ':'.join(re.findall('..', address))
        return cls._address.lower()

    @abc.abstractmethod
    def _decode_naa5(self):
        """ Method used for decoding NAA5 WWN """

    @abc.abstractmethod
    def _decode_naa6(self):
        """ Method used for decoding NAA6 WWN """

    def __eq__(self, other):
        # if the other object is a 'str', we try a conversion
        if isinstance(other, str):
            try:
                other = WWN(other)

            except WWNInvalidError:
                return False

        elif not isinstance(other, WWN):
            return False

        return self._address == other._address

    def __repr__(self):
        return f"<{self.__class__.__name__}({self._address})>"

    def __str__(self):
        # By convention the NAA5 WWNs are represented with ':', NAA6 not
        return self.wwn if not self._address[0] == '6' else self.wwn_nodots

    @property
    def decode(self):
        """
        Extract the data encoded in the WWN
        :return: Data encoded in the WWN
        :rtype: str
        """
        return self._decode

    @property
    def oui(self):
        """
        Get the OUI (Organization Unique Identifier) of the WWN
        :return: OUI string
        :rtype: str
        """
        oui = ''
        first_digit = self._address[0]

        if first_digit not in ('1', '2', '5', '6', 'c'):
            raise WWNInvalidError('No normalized NAA')

        if first_digit in ('1', '2'):
            oui = self.wwn_nodots[4:10]

        if first_digit in ('5', '6'):
            oui = self.wwn_nodots[1:8]

        # AIX NPIV special case (all NPIV LPAR WWN starts by 'c0')
        if first_digit == 'c':
            oui = '0' + self.wwn_nodots[1:6]

        return ':'.join(re.findall('..', oui))

    @property
    def wwn(self):
        """ Get the normalized WWN string """
        return self._address

    @property
    def wwn_nodots(self):
        """ Get the WWN string without colons """
        return self._address.replace(':', '')

    @property
    def wwn_to_binary(self):
        """ Get the WWN encoded to binary form """
        return bin(int(self.wwn_nodots, 16))[2:]
