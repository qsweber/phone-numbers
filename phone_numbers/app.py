import datetime
import logging

from flask import Flask, request, jsonify

from phone_numbers.clients.s3 import S3Client
from phone_numbers.words import WORDS
from phone_numbers.lib.words import get_new_words
from phone_numbers.lib.trie import Trie
from phone_numbers.lib.sentence_creator import make_sentence_from_numbers
from phone_numbers.lib.s3_cache import s3_cache

app = Flask(__name__)
logger = logging.getLogger(__name__)

s3_client = S3Client()


@s3_cache(s3_client, 'qsweber-temp', 'phone-numbers/trie')
def get_trie():
    return Trie(WORDS)


@s3_cache(s3_client, 'qsweber-temp', 'phone-numbers/trie_new')
def get_trie_new():
    return Trie(get_new_words(WORDS))


@app.route('/api/v0/match', methods=['GET'])
def index():
    time1 = datetime.datetime.now()

    trie = get_trie()
    time2 = datetime.datetime.now()

    trie_new = get_trie_new()
    time3 = datetime.datetime.now()

    string = request.args['value']

    match = make_sentence_from_numbers(trie, string)
    time4 = datetime.datetime.now()

    match_new = make_sentence_from_numbers(trie_new, string)
    time5 = datetime.datetime.now()

    logger.info('time1: {}, time2: {}, time3: {}, time4: {}, time5: {}'.format(
        time1.isoformat(),
        time2.isoformat(),
        time3.isoformat(),
        time4.isoformat(),
        time5.isoformat(),
    ))

    response = jsonify({
        'input': string,
        'match': match,
        'match_new': match_new,
    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response
