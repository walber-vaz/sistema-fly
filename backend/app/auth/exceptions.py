from app.auth.constants import ErrorMessage
from app.exceptions import NotAuthenticated, PermissionDenied


class NotAuthenticatedException(NotAuthenticated):
    DETAIL = ErrorMessage.NOT_AUTHENTICATED


class PermissionDeniedException(PermissionDenied):
    DETAIL = ErrorMessage.EMAIL_OR_PASSWORD_INVALID
