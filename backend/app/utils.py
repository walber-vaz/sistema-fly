from enum import Enum
from random import randint
from uuid import uuid4


class RoleEnum(Enum):
    ADMIN = 'admin'
    CUSTOMER = 'customer'


def pagination(total: int, page: int, per_page: int) -> dict:
    total_pages = total // per_page
    if total % per_page > 0:
        total_pages += 1

    has_next = page < total_pages
    has_previous = page > 1
    has_last_page = total_pages > 1

    next_page = page + 1 if has_next else None
    previous_page = page - 1 if has_previous else None
    last_page = total_pages if has_last_page else None

    return {
        'total': total,
        'page': page,
        'per_page': per_page,
        'total_pages': total_pages,
        'has_next': has_next,
        'has_previous': has_previous,
        'has_last_page': has_last_page,
        'next_page': next_page,
        'last_page': last_page,
        'previous_page': previous_page,
    }


def generate_code_product() -> str:
    return str(uuid4().hex)[:8].upper()


def generate_barcode() -> str:
    digit = [str(randint(0, 9)) for _ in range(12)]

    sum_even = sum(int(d) for d in digit[::2])
    sum_odd = sum(int(d) for d in digit[1::2]) * 3
    total = sum_even + sum_odd

    digit_check = (10 - (total % 10)) % 10
    digit.append(str(digit_check))

    code = ''.join(digit)

    return code
