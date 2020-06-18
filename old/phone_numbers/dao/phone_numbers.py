from phone_numbers.dao.base import Dao
from phone_numbers.models.phone_numbers import PhoneNumber


class PhoneNumbersDao(Dao):
    def __init__(self):
        super(PhoneNumbersDao, self).__init__(PhoneNumber, 'phone_numbers')
