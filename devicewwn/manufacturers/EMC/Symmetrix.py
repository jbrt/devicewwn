#!/usr/bin/env python3
# coding: utf-8

"""
EMC WWN (Symmetrix & VMAX)
"""

import binascii
from devicewwn.wwn import WWN, WWNInvalidError


class EmcDmxWWNError(WWNInvalidError):
    """
    Generic DMX Exception
    """
    def __init__(self, value):
        super(EmcDmxWWNError, self).__init__("Invalid DMX WWN: {0!r}".
                                             format(value))


class EmcDmxWWN(WWN):
    """
    Decode WWN from EMC DMX Arrays
    Based on EMC KB Articles: 000323236(DMX) and 000322895
    """
    processor = {'00': 'A',
                 '01': 'B',
                 '10': 'C',
                 '11': 'D'}

    def __init__(self, address):
        super(EmcDmxWWN, self).__init__(address)

        if not self.oui == '00:60:48':
            raise EmcDmxWWNError('This not a WWN DMX !')

    def _decodeNaa5(self):
        digit = self.wwn_to_binary
        half_bit = digit[27]
        side_bit = digit[57]
        serial = digit[28:57]
        port_bit = digit[58]
        slot_bit = digit[59:]

        self._decode = 'DMX S/N:%d Dir:%d%s Port:%s' % (int(serial, 2),
                                                        int(slot_bit, 2)+1,
                                                        self.processor[half_bit+side_bit],
                                                        'A' if port_bit == '0' else 'B')

    def _decodeNaa6(self):
        serial = self.wwn_nodots[8:20]
        hve = str(binascii.unhexlify(self.wwn_nodots[-12:]), 'UTF-8')
        self._decode = 'DMX S/N:%s HVE:%s' % (serial, hve)

    
class EmcVmaxWWNError(WWNInvalidError):
    """
    Generic VMAX Exception
    """
    def __init__(self, value):
        super(EmcVmaxWWNError, self).__init__("Invalid VMAX WWN: {0!r}".
                                              format(value))


class EmcVmaxWWN(WWN):
    """
    Decode WWN from EMC VMAX, VMAX2 and VMAX3 Arrays
    Based on EMC KB Articles: 000323234(VMAX3) and 000333474(VMAX1&2)
    """

    # Bits that's describe the VMAX location
    location = {'001': 'HK19', '010': 'CK29', '100': 'CN49'}

    vtype = {'101010': '67',
             '101011': '68',
             '101111': '72',
             '0000010': '26',
             '0110000': '49',
             '1000000': '57',
             '1000100': '59',
             '1111100': '87'}

    vmodel = {'101010': 'VMAX3-200K',
              '101011': 'VMAX3-100K',
              '101111': 'VMAX3-400K',
              '0000010': 'VMAX-20K',
              '0110000': 'VMAX-SE',
              '1000000': 'VMAX-40K',
              '1000100': 'VMAX-10K',
              '1111100': 'VMAX-10K'}

    vdir_letter = {'0000': 'A', '0001': 'B', '0010': 'C', '0011': 'D',
                   '0100': 'E', '0101': 'F', '0110': 'G', '0111': 'H'}

    vmax2_mask = {'vtype': slice(30, 37),
                  'vmodel': slice(30, 37),
                  'serial': slice(37, 53),
                  'director': slice(57, 61),
                  'port': slice(61, 63)}

    vmax3_mask = {'vtype': slice(30, 36),
                  'vmodel': slice(30, 36),
                  'serial': slice(36, 53),
                  'director': slice(53, 57),
                  'port': slice(57, 63)}

    def __init__(self, address):
        super(EmcVmaxWWN, self).__init__(address)
     
        if not self.oui == '00:00:97':
            raise EmcVmaxWWNError('This not a WWN Vmax !')

    def _decodeNaa5(self):
        digit = self.wwn_to_binary
        location = self.location[digit[27:30]] if digit[27:30] in self.location else '(Unknown)'

        mask = self.vmax3_mask if digit[30:33] == '101' else self.vmax2_mask

        vtype = self.vtype[digit[mask['vtype']]] if digit[mask['vtype']] else '(Unknown)'
        model = self.vmodel[digit[mask['vmodel']]] if digit[mask['vmodel']] else '(Unknown)'
        serial = "%05d" % int(digit[mask['serial']], 2)
        director = str(int(digit[mask['director']], 2)+1)
        port = str(int(digit[mask['port']], 2))
        
        # if mask is vmax2: then we need to extract letter
        letter = ''
        if mask is self.vmax2_mask:
            letter = self.vdir_letter[digit[53:57]] if digit[53:57] in self.vdir_letter else '(Unknown)'

        self._decode = "%s S/N:%s%s%s Dir:%s%s Port:%s" % (model, location,
                                                           vtype, serial,
                                                           director, letter,
                                                           port)

    def _decodeNaa6(self):
        serial = self.wwn_nodots[8:20]
        vmax_model = ('26', '49', '57', '59', '87')

        # Offset on VMAX and VMAX2 = 8 / VMAX3 = 10
        # because HVE VMAX1 & 2 == 4 char. / VMAX == 5 char.
        offset = 8 if serial[5:7] in vmax_model else 10
        model = 'VMAX' if serial[5:7] in vmax_model else 'VMAX3'
        hve = str(binascii.unhexlify(self.wwn_nodots[-offset:]), 'UTF-8')
        self._decode = '%s S/N:%s HVE:%s' % (model, serial, hve)
