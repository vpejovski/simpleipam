import os
import json
import ipcalc
import ipam.exception

class FileSystemStore(object):
    """docstring for FileSystemStore"""

    def __init__(self, path=None, file_name=None):
        super(FileSystemStore, self).__init__()
        self._path = path
        self._file_name = file_name
        self._file_store = None
        self._data_store = None

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, path):
        self._path = path

    @property
    def file_name(self):
        return self._file_name

    @file_name.setter
    def file_name(self, file_name):
        self._file_name = file_name

    def _load_database(self):
        if self._data_store is None:
            if (self._file_name is not None) and (self._path is not None):
                with open(os.path.join(self._path, self._file_name), 'r') as config_file:
                    self._data_store = json.load(config_file)


    def _get_datastore(self):
        if self._path is None or self._file_name is None:
            raise ipam.exception.ParameterMissingError("File name and path are empty.")

        if self._data_store is None:
            self._load_database()

        return self._data_store


    def _get_network(self, network=None):
        if network is None:
            network_key = sorted(self._data_store.keys())[0]
        else:
            network_key = network

        network = ipcalc.Network(network_key)
        return network, network_key

    def get_ip_address(self, hostname, mac_address, network=None):
        '''
            Return a first free ip address from either specified network
            or default network (first one in sorted list).
        '''
        if self._data_store is None:
            self._load_database()

        network, network_key = self._get_network()

        network_hosts = sorted(self._data_store[self._data_store.keys()[0]].keys())

        for ip_address in network:
            if ip_address not in network_hosts:
                self._data_store[network_key][str(ip_address)] = [hostname, mac_address]
                return str(ip_address)

    def release_ip_address(self, ip_address, hostname, mac_address, network=None):
        if network is None:
            network, network_key = self._get_network()

        if ip_address in self._data_store[network_key]:
            if hostname == self._data_store[network_key][ip_address][0] and mac_address == self._data_store[network_key][ip_address][1]:
                del self._data_store[network_key][ip_address]


    def get_assigned_ip_addresses(self, network=None):
        data_store = self._get_datastore()

        network, network_key = self._get_network(network)

        return sorted(data_store[network_key].keys())