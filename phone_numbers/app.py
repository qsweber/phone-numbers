from flask import Flask, request, jsonify

from phone_numbers.words import WORDS
from phone_numbers.lib.words import get_new_words
from phone_numbers.lib.trie import Trie
from phone_numbers.lib.sentence_creator import make_sentence_from_numbers

app = Flask(__name__)


@app.route('/api/v0/match', methods=['GET'])
def index():
    trie = Trie(WORDS)
    trie_new = Trie(get_new_words(WORDS))

    string = request.args['value']

    match = make_sentence_from_numbers(trie, string)
    match_new = make_sentence_from_numbers(trie_new, string)

    response = jsonify({
        'input': string,
        'match': match,
        'match_new': match_new,
    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response
