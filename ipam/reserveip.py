import ipcalc
import ipam.exception


class ReserveIP (object):
    """
    Provides the ability to reserve ip addresses before actually
    having host names and MAC addresses.
    """
    def __init__(self, data_store=None):
        super(ReserveIP, self).__init__()
        self._data_store = data_store

