
class RequestError(Exception):

    def __init__(self, message="failed to request data"):
        Exception.__init__(self, message)


class ParamError(Exception):

    def __init__(self, message="invalid param"):
        Exception.__init__(self, message)
