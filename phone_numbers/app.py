import datetime
import logging

from flask import Flask, request, jsonify

from phone_numbers.words import WORDS
from phone_numbers.lib.words import get_new_words
from phone_numbers.lib.trie import Trie
from phone_numbers.lib.sentence_creator import make_sentence_from_numbers

app = Flask(__name__)
logger = logging.getLogger(__name__)


@app.route('/api/v0/match', methods=['GET'])
def index():
    time1 = datetime.datetime.now()

    trie = Trie(WORDS)
    time2 = datetime.datetime.now()

    trie_new = Trie(get_new_words(WORDS))
    time3 = datetime.datetime.now()

    string = request.args['value']

    match = make_sentence_from_numbers(trie, string)
    time4 = datetime.datetime.now()

    match_new = make_sentence_from_numbers(trie_new, string)
    time5 = datetime.datetime.now()

    logger.info('time1: {}, time1: {}, time1: {}, time1: {}, time1: {}'.format(
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
