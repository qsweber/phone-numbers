import datetime
from decimal import Decimal
import logging

from flask import Flask, request, jsonify

from phone_numbers.clients.s3 import S3Client
from phone_numbers.models.phone_numbers import PhoneNumber
from phone_numbers.lib.trie import Trie
from phone_numbers.lib.sentence_creator_fast import make_sentence_from_numbers, clean_input
from phone_numbers.lib.s3_cache import s3_cache

app = Flask(__name__)
logger = logging.getLogger(__name__)

s3_client = S3Client()


@s3_cache(s3_client, 'qsweber-temp', 'phone-numbers/trie-extended')
def get_trie():
    with open('/usr/share/dict/words') as fh:
        words = [
            word.strip()
            for word in fh.readlines()
        ]

    return Trie(words)


trie = get_trie()


def calculate(input_phone_number: str) -> PhoneNumber:
    start_time = datetime.datetime.now()

    result = make_sentence_from_numbers(trie, input_phone_number)

    phone_number = PhoneNumber(
        phone_number=input_phone_number,
        phone_number_sanitized=clean_input(input_phone_number),
        result=result,
        seconds=round(Decimal((datetime.datetime.now() - start_time).total_seconds()), 3),
        created_at=datetime.datetime.now(),
    )

    return phone_number


@app.route('/api/v0/match', methods=['GET'])
def index():
    input_phone_number = request.args['value']
    phone_number = calculate(input_phone_number)

    response = jsonify({
        'input': input_phone_number,
        'match': phone_number.result,
    })

    response.headers.add('Access-Control-Allow-Origin', '*')

    return response
