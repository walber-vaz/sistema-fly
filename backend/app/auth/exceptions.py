from app.auth.constants import ErrorMessage
from app.exceptions import Forbidden, NotAuthenticated, PermissionDenied


class NotAuthenticatedException(NotAuthenticated):
    DETAIL = ErrorMessage.NOT_AUTHENTICATED


class PermissionDeniedException(PermissionDenied):
    DETAIL = ErrorMessage.EMAIL_OR_PASSWORD_INVALID


class ForbiddenException(Forbidden):
    DETAIL = ErrorMessage.FORBIDDEN
