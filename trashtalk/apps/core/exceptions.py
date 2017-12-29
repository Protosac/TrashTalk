# pylint: disable=missing-docstring


# pylint: disable=missing-docstring
class TrashTalkError(Exception):
    _code = 'TRASHTALK_ERROR'

    def __init__(self, message, code=_code, base_exception=None):
        """

        :param msg: `str`, error message
        :param code: `str`used for logging and error aggregation
        """
        self.message = message
        self.code = code
        self.base_exception = base_exception
        super(TrashTalkError, self).__init__(message)

    def __str__(self):
        return "{0} - {1}".format(self.code, self.message)


class TrashtalkQueryError(TrashTalkError):
    pass


class TrashTalkHTTPError(TrashTalkError):
    def __init__(self, message, status=None, url=None, detail=None, **kwargs):
        """

        :param msg: `str`, error message
        :param code: `str`used for logging and error aggregation
        :param status: `int`, HTTP status code if available
        :param url: `str`, endpoint last accessed when this error occured
        :param detail: any additional information about the error
        """
        self.status = status
        self.url = url
        self.detail = detail
        self.options = kwargs
        # Python 2 style:
        # super(TrashTalkError, self).__init__(message)
        super()

    def __str__(self):
        return "{0} - {1}\n Status: {2}\n URL: {3}\n Detail: {4}".format(self.code,
                                                                         self.message,
                                                                         self.status,
                                                                         self.url,
                                                                         self.detail)
