class Error(Exception):
    """ipam module exception base"""
    pass

class ParameterMissingError(Error):
    """Exception raised when class init info is missing."""
    pass
