class InvalidTypeError(BaseException):
    """
    Used to represent an Invalid Type
    """


class InvalidHandlerErr(BaseException):
    """
    Used when bad Handler is request.
    """


class ParamSchemaValidationError(BaseException):
    """
    Used when Handlers fails param schema validation
    """