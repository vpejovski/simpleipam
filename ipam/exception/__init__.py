class Error(Exception):
    """ipam module exception base"""
    pass

class ParameterMissingError(Error):
    """Exception raised when class init info is missing."""
    pass

class DuplicateAssignmentError(Error):
    """
    Exception raised when you try to acquire ip address but its already
    in database.
    """
    pass

class UnknownAssignmentError(Error):
    """
    Exception raised when you try to release ip address but it is not
    in database.
    """
    pass

class NoMatchAssignmentError(Error):
    """
    Exception raised when you try to release ip that is assigned to a
    different host in database.
    """
    pass

class FileUpdateError(Error):
    """docstring for FileUpdateError"""
    pass