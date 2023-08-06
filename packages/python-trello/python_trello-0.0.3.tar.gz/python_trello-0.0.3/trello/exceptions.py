class Error(Exception):
    pass


class MovedURL(Error):
    """
    Exception to raise when the website has moved to a different location
    """
    pass


class HorriblyGoneWrongError(Error):
    """
    Exception to raise when there is something wrong gone which is difficult to comprehend
    """
    pass


class ResponseNotOKError(Error):
    """
    Exceptions to raise when the response is somthing other than 200
    """
    pass
