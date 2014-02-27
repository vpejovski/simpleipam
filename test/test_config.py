import unittest
from nose.tools import *  # PEP8 asserts
import ipcalc
import os

import sys
sys.path.append('../')

try:
    import ipam.config
except Exception, e:
    raise e


class ConfigTest(unittest.TestCase):

    '''An unit test case for ipam data store.'''

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_create_file_store(self):
        file_store = ipam.config.FileSystemStore()
        assert_is_not_none(file_store)

    def test_set_path(self):
        file_store = ipam.config.FileSystemStore()
        file_store.path = '/etc/ipam/'
        assert_equal('/etc/ipam/', file_store.path)

    def test_set_file_name(self):
        file_store = ipam.config.FileSystemStore()
        file_store.file_name ='ipam_db'
        assert_equal('ipam_db', file_store.file_name)

    def test_get_ip_address(self):
        file_store = ipam.config.FileSystemStore(path=os.path.realpath(os.path.curdir), file_name='ipam_db')
        ip_address = file_store.get_ip_address('hostname', 'mac_address')
        assert_is_not_none(ip_address)

    def test_get_ip_address_check_duplicate(self):
        file_store = ipam.config.FileSystemStore(path=os.path.realpath(os.path.curdir), file_name='ipam_db')
        ip_address_1 = file_store.get_ip_address('hostname1', 'mac_address1')
        ip_address_2 = file_store.get_ip_address('hostname2', 'mac_address2')
        assert_not_equal(ip_address_1, ip_address_2)


if __name__ == '__main__':
    unittest.main()