class DuplicateEntryException(Exception):
    """Duplicate row exception"""

    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)
