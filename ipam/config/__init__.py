import os
import json
import ipcalc

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
            with open(os.path.join(self._path, self._file_name), 'r') as config_file:
                self._data_store = json.load(config_file)


    def get_ip_address(self, hostname, mac_address, network=None):
        if self._data_store is None:
            self._load_database()

        if network is None:
            network = ipcalc.Network(self._data_store.keys()[0])
            for ip_address in network:
                if ip_address not in self._data_store[self._data_store.keys()[0]].keys():
                    return str(ip_address)

