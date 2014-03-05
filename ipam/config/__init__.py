import os
import json
import ipcalc
import ipam.exception
import threading


class DataStore(object):
    """Base class for DataStore"""

    def __init__(self):
        super(DataStore, self).__init__()
        self._data_store = None
        self._rlock = threading.RLock()

    def get_datastore(self):
        pass

    def assign_ip(self, network, ip_address, hostname, mac_address):
        raise NotImplementedError

    def release_ip(self, network, ip_address, hostname, mac_address):
        raise NotImplementedError

    def assigned_ips(self, network):
        raise NotImplementedError

    def persist_datastore(self):
        pass

    def _acquire_lock(self):
        return self._rlock.acquire()

    def _release_lock(self):
        self._rlock.release()


class FileSystemStore(DataStore):
    """doc string for FileSystemStore"""

    def __init__(self, path=None, file_name=None):
        super(FileSystemStore, self).__init__()
        self._path = path
        self._file_name = file_name

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

    def get_datastore(self):
        if self._path is None or self._file_name is None:
            raise ipam.exception.ParameterMissingError("File name and path are empty.")

        if self._data_store is None:
            self._load_database()

        return self._data_store

    def get_network(self, network=None):
        self.get_datastore()

        if network is None:
            network_key = sorted(self._data_store.keys())[0]
        else:
            network_key = network

        network = ipcalc.Network(network_key)
        return network, network_key

    def assign_ip(self, network, ip_address, hostname, mac_address):
        """
        Makes assignment to DataStore permanent.
        """
        self.get_datastore()
        if ip_address in self._data_store[network]:
            raise ipam.exception.DuplicateAssignmentError("Ip address already assigned.")

        self._data_store[network][ip_address] = [hostname, mac_address]
        self.persist_datastore()

    def release_ip(self, network, ip_address, hostname, mac_address):
        """
        Release already assigned ip.
        """
        self.get_datastore()
        if ip_address in self._data_store[network]:
            if hostname == self._data_store[network][ip_address][0] and mac_address == self._data_store[network][ip_address][1]:
                del self._data_store[network][ip_address]
            else:
                raise ipam.exception.NoMatchAssignmentError("Ip address assigned to a different host.")
        else:
            raise ipam.exception.UnknownAssignmentError("Ip address is not found in database.")
        self.persist_datastore()

    def assigned_ips(self, network):
        self.get_datastore()
        network, network_key = self.get_network(network)
        return sorted(self._data_store[network_key].keys())

    def persist_datastore(self):
        if self._acquire_lock():
            with open(os.path.join(self._path, self._file_name), 'wb') as config_file:
                json.dump(self._data_store, config_file, indent=4, encoding="utf-8", sort_keys=True)
            self._release_lock()
        else:
            raise ipam.exception.FileUpdateError
