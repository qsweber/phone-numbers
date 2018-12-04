from decimal import Decimal
from typing import NamedTuple


class PhoneNumber(NamedTuple):
    phone_number: str
    result: str
    seconds: Decimal
