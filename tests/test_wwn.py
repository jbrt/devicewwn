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
