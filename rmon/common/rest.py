"""rmon.common.rest
"""

class RestException(Exception):
    """abnormal base class
    """

    def __init__(self, code, message):
        """initialize abnormal

         Aargs:
             code(int): http status code
             message(str): error message

        """
        self.code = code
        self.message = message
        super(RestException, self).__init__()
