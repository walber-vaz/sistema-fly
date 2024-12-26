from app.exceptions import BadRequest, NotFound
from app.product.constants import ErrorMessages


class ProductAlreadyExists(BadRequest):
    DETAIL = ErrorMessages.PRODUCT_EXISTS


class ProductNotFound(NotFound):
    DETAIL = ErrorMessages.PRODUCT_NOT_FOUND


class ProductNotOwner(BadRequest):
    DETAIL = ErrorMessages.PRODUCT_NOT_OWNER


class ProductImageNotSupported(BadRequest):
    DETAIL = ErrorMessages.PRODUCT_IMAGE_NOT_SUPPORTED
