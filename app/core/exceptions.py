
class AppError(Exception):
    code: str = "APP_ERROR"
    message: str = "Application error"
    
    def __init__(self, detail: str | None = None):
        super().__init__(detail)
        self.detail = detail
    
class NotFoundError(AppError):
    code = "NOT_FOUND"
    message = "Resource not found"
    
class ConflictError(AppError):
    code = "CONFLICT"
    message = "Conflict"
    
class UnauthorizedError(AppError):
    code = "UNAUTHORIZED"
    message = "Unauthorized"
    
class ForbiddenError(AppError):
    code = "FORBIDDEN"
    message = "Forbidden"
    
class BadRequestError(AppError):
    code = "BAD_REQUEST"
    message = "Bad request"
    
class TooManyRequestsError(AppError):
    code = "TOO_MANY_REQUESTS"
    message = "Too many requests"
