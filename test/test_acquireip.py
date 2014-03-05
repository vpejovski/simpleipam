import unittest
from nose.tools import *  # PEP8 asserts
import ipcalc
import os

import sys
sys.path.append('../')

try:
    import ipam.config
    import ipam.exception
    import ipam.acquireip
except Exception, e:
    raise e


class AcquireIPTest(unittest.TestCase):

    '''An unit test case for ipam data store.'''

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_ip_address(self):
        file_store = ipam.config.FileSystemStore(path=os.path.realpath(os.path.curdir), file_name='ipam_db')
        ipmanager = ipam.acquireip.AcquireIP(data_store=file_store)
        ip_address = ipmanager.get_ip_address('hostname', 'mac_address')
        assert_is_not_none(ip_address)

    def test_get_ip_address_with_network(self):
        file_store = ipam.config.FileSystemStore(path=os.path.realpath(os.path.curdir), file_name='ipam_db')
        ipmanager = ipam.acquireip.AcquireIP(data_store=file_store)
        ip_address = ipmanager.get_ip_address('hostname', 'mac_address', network="192.168.1.0/24")
        assert_is_not_none(ip_address)

    def test_get_ip_address_check_duplicate(self):
        file_store = ipam.config.FileSystemStore(path=os.path.realpath(os.path.curdir), file_name='ipam_db')
        ipmanager = ipam.acquireip.AcquireIP(data_store=file_store)

        ip_address_1 = ipmanager.get_ip_address('hostname1', 'mac_address1')
        ip_address_2 = ipmanager.get_ip_address('hostname2', 'mac_address2')
        assert_not_equal(ip_address_1, ip_address_2)

    def test_release_ip_address(self):
        file_store = ipam.config.FileSystemStore(path=os.path.realpath(os.path.curdir), file_name='ipam_db')
        ipmanager = ipam.acquireip.AcquireIP(data_store=file_store)

        ip_address_1 = ipmanager.get_ip_address('hostname1', '08:00:27:59:ab:61')
        ip_address_2 = ipmanager.get_ip_address('hostname2', '08:00:27:59:ab:62')

        ipmanager.release_ip_address(ip_address_2, 'hostname2', '08:00:27:59:ab:62')
        ip_address_3 = ipmanager.get_ip_address('hostname2', '08:00:27:59:ab:62')
        assert_equal(ip_address_2, ip_address_3)

    def test_get_assigned_ips(self):
        file_store = ipam.config.FileSystemStore(path=os.path.realpath(os.path.curdir), file_name='ipam_db')
        ipmanager = ipam.acquireip.AcquireIP(data_store=file_store)
        assigned_ip_list = ipmanager.get_assigned_ip_addresses()
        assert_equal(1, len(assigned_ip_list))

    def test_get_assigned_ips(self):
        file_store = ipam.config.FileSystemStore(path=os.path.realpath(os.path.curdir), file_name='ipam_db')
        ipmanager = ipam.acquireip.AcquireIP(data_store=file_store)
        assigned_ip_list = ipmanager.get_assigned_ip_addresses()
        assert_equal(1, len(assigned_ip_list))

        ip_address_1 = ipmanager.get_ip_address('hostname1', '08:00:27:59:ab:61')
        assigned_ip_list = ipmanager.get_assigned_ip_addresses()
        assert_equal(2, len(assigned_ip_list))

    @raises(ipam.exception.ParameterMissingError)
    def test_empty_parameter(self):
        file_store = ipam.config.FileSystemStore()
        ipmanager = ipam.acquireip.AcquireIP(data_store=file_store)
        assigned_ip_list = ipmanager.get_assigned_ip_addresses()
