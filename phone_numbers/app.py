from flask import Flask, request, jsonify

from phone_numbers.words import WORDS
from phone_numbers.lib.trie import Trie
from phone_numbers.lib.sentence_creator import make_sentence_from_numbers

app = Flask(__name__)


@app.route('/api/v0/match', methods=['GET'])
def index():
    trie = Trie(WORDS)

    string = request.args['value']

    match = make_sentence_from_numbers(trie, string)

    response = jsonify({
        'input': string,
        'match': match,
    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response
