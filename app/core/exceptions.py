class AppException(Exception):
    def __init__(self, code: int, error_type: str, message: str):
        self.code = code
        self.error_type = error_type
        self.message = message


class BadRequestError(AppException):
    def __init__(self, message: str = "Bad Request"):
        super().__init__(400, "BAD_REQUEST", message)


class UnauthorizedError(AppException):
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(401, "UNAUTHORIZED", message)


class ForbiddenError(AppException):
    def __init__(self, message: str = "Forbidden"):
        super().__init__(403, "FORBIDDEN", message)


class NotFoundError(AppException):
    def __init__(self, message: str = "Not Found"):
        super().__init__(404, "NOT_FOUND", message)


class MethodNotAllowedError(AppException):
    def __init__(self, message: str = "Method Not Allowed"):
        super().__init__(405, "METHOD_NOT_ALLOWED", message)


class UnprocessableError(AppException):
    def __init__(self, message: str = "Unprocessable Entity"):
        super().__init__(422, "UNPROCESSABLE_ENTITY", message)
