from .log import logger


class MlChainError(Exception):
    """Base class for all exceptions."""

    def __init__(self, msg, code='exception', status_code=500):
        self.msg = msg
        self.code = code
        self.status_code = status_code
        logger.error("[{0}]: {1}".format(code, msg))


class MLChainAssertionError(MlChainError):
    def __init__(self, msg, code="assertion", status_code=422):
        MlChainError.__init__(self, msg, code, status_code)


class MLChainSerializationError(MlChainError):
    def __init__(self, msg, code="serialization", status_code=422):
        MlChainError.__init__(self, msg, code, status_code)
