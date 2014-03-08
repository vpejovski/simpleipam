import unittest
from nose.tools import *  # PEP8 asserts
import ipcalc
import os

import sys
sys.path.append('../')

try:
    import ipam.config
    import ipam.exception
    import ipam.reserveip
except Exception, e:
    raise e


class ReserveIPTest(unittest.TestCase):

    '''Test IP reservation module.'''

    def setUp(self):
        with open(os.path.join(os.path.realpath(os.path.curdir), 'ipam_db'), 'wb') as config_file:
            config_file.write('{"192.168.1.0/24": {"192.168.1.1": ["gateway", "ff:ff:ff:ff:ff:ff:ff:ff"]}}')

    def teardown(self):
        os.remove(os.path.join(os.path.realpath(os.path.curdir), 'ipam_db'))

    def test_constructor(self):
        reserve = ipam.reserveip.ReserveIP(None)
        assert_is_not_none(reserve)


if __name__ == '__main__':
    unittest.main()