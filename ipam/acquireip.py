import ipcalc
import ipam.exception


class AcquireIP (object):
    """AcquireIP contains the functions for ip address management."""
    def __init__(self, data_store=None):
        super(AcquireIP, self).__init__()
        self._data_store = data_store

    def get_ip_address(self, hostname, mac_address, network=None):
        """
        Return a first free ip address from either specified network
        or default network (first one in sorted list).
        """

        network, network_key = self._data_store.get_network(network)
        network_hosts = self.get_assigned_ip_addresses(network_key)

        for ip_address in network:
            if ip_address not in network_hosts:
                self._data_store.assign_ip(network_key, str(ip_address), hostname, mac_address)
                # self._data_store.get_datastore()[network_key][str(ip_address)] = [hostname, mac_address]
                return str(ip_address)

    def release_ip_address(self, ip_address, hostname, mac_address, network=None):
        if network is None:
            network, network_key = self._data_store.get_network(network)

        self._data_store.release_ip(network_key, ip_address, hostname, mac_address)

    def get_assigned_ip_addresses(self, network=None):
        """
        Returns all current assignments for network.
        """
        return self._data_store.assigned_ips(network)


