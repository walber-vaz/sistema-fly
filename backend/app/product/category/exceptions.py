from app.exceptions import BadRequest
from app.product.category.constants import ErrorMessage


class CategoryAlreadyExists(BadRequest):
    DETAIL = ErrorMessage.CATEGORY_ALREADY_EXISTS


class CategoryNotFound(BadRequest):
    DETAIL = ErrorMessage.CATEGORY_NOT_FOUND


class CategoryNotOwner(BadRequest):
    DETAIL = ErrorMessage.CATEGORY_NOT_OWNER
