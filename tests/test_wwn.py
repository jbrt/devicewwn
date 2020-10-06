# coding: utf-8

"""
Unittest for WWN class
"""

from devicewwn.factory import WWNFactory

FACTORY = WWNFactory()


def test_symmetrix_dmx_wwn():
    wwn = FACTORY.create('50:06:04:8c:52:a6:6d:86')
    assert wwn.wwn == '50:06:04:8c:52:a6:6d:86'
    assert wwn.oui == '00:60:48'
    assert wwn.decode == 'DMX S/N:290101686 Dir:7C Port:A'


def test_hitachi_wwn():
    wwn = FACTORY.create('60060e8012b23e005040b23e00002245')
    assert wwn.wwn == '60:06:0e:80:12:b2:3e:00:50:40:b2:3e:00:00:22:45'
    assert wwn.oui == '00:60:e8'
    assert wwn.decode == 'Hitachi S/N:45630 HVE:22:45'
