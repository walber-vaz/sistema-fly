from app.exceptions import BadRequest
from app.product.brand.constants import ErrorMessage


class BrandAlreadyExists(BadRequest):
    DETAIL = ErrorMessage.BRAND_ALREADY_EXISTS


class BrandNotFound(BadRequest):
    DETAIL = ErrorMessage.BRAND_NOT_FOUND


class BrandNotOwner(BadRequest):
    DETAIL = ErrorMessage.BRAND_NOT_OWNER
