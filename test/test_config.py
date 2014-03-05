import unittest
from nose.tools import *  # PEP8 asserts
import ipcalc
import os

import sys
sys.path.append('../')

try:
    import ipam.config
    import ipam.exception
except Exception, e:
    raise e


class ConfigTest(unittest.TestCase):

    '''An unit test case for ipam data store.'''

    def setUp(self):
        with open(os.path.join(os.path.realpath(os.path.curdir), 'ipam_db'), 'wb') as config_file:
            config_file.write('{"192.168.1.0/24": {"192.168.1.1": ["gateway", "ff:ff:ff:ff:ff:ff:ff:ff"]}}')

    def teardown(self):
        os.remove(os.path.join(os.path.realpath(os.path.curdir), 'ipam_db'))

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

    def test_release_ip(self):
        file_store = ipam.config.FileSystemStore(path=os.path.realpath(os.path.curdir), file_name='ipam_db')
        file_store.release_ip("192.168.1.0/24", "192.168.1.1", "gateway", "ff:ff:ff:ff:ff:ff:ff:ff")

    @raises(ipam.exception.UnknownAssignmentError)
    def test_release_ip_non_existent(self):
        file_store = ipam.config.FileSystemStore(path=os.path.realpath(os.path.curdir), file_name='ipam_db')
        file_store.release_ip("192.168.1.0/24", "192.168.1.2", "gateway2", "ff:ff:ff:ff:ff:ff:ff:ff")

    @raises(ipam.exception.NoMatchAssignmentError)
    def test_release_ip_diff_host_name(self):
        file_store = ipam.config.FileSystemStore(path=os.path.realpath(os.path.curdir), file_name='ipam_db')
        file_store.release_ip("192.168.1.0/24", "192.168.1.1", "gateway2", "ff:ff:ff:ff:ff:ff:ff:ff")

    @raises(ipam.exception.DuplicateAssignmentError)
    def test_assign_ip_duplicate(self):
        file_store = ipam.config.FileSystemStore(path=os.path.realpath(os.path.curdir), file_name='ipam_db')
        file_store.assign_ip("192.168.1.0/24", "192.168.1.1", "gateway", "ff:ff:ff:ff:ff:ff:ff:ff")

    @raises(ipam.exception.FileUpdateError)
    def test_persist_datastore_error(self):
        file_store = ipam.config.FileSystemStore(path=os.path.realpath(os.path.curdir), file_name='ipam_db')
        def f() : return False
        file_store._acquire_lock = f
        file_store.assign_ip("192.168.1.0/24", "192.168.1.2", "gateway2", "ff:ff:ff:ff:ff:ff:ff:fe")


if __name__ == '__main__':
    unittest.main()
