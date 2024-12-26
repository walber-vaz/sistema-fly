from app.exceptions import BadRequest
from app.user.constants import ErrorMessage


class LengthPhoneException(BadRequest):
    DETAIL = ErrorMessage.LENGTH_PHONE_NUMBER


class LengthFirstNameException(BadRequest):
    DETAIL = ErrorMessage.LENGTH_FIRST_NAME


class LengthSurnameException(BadRequest):
    DETAIL = ErrorMessage.LENGTH_SURNAME


class PasswordRequirementsException(BadRequest):
    DETAIL = ErrorMessage.PASSWORD_REQUIREMENTS


class EmailAlreadyRegisteredException(BadRequest):
    DETAIL = ErrorMessage.EMAIL_ALREADY_REGISTERED


class PhoneNumberAlreadyRegisteredException(BadRequest):
    DETAIL = ErrorMessage.PHONE_NUMBER_ALREADY_REGISTERED


class ErrorCreateUserException(BadRequest):
    DETAIL = ErrorMessage.ERROR_CREATE_USER


class UserNotFoundException(BadRequest):
    DETAIL = ErrorMessage.USER_NOT_FOUND
