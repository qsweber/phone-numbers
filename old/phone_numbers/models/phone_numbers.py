from datetime import datetime
from decimal import Decimal
from typing import NamedTuple


class PhoneNumber(NamedTuple):
    phone_number: str
    phone_number_sanitized: str
    result: str
    seconds: Decimal
    created_at: datetime
