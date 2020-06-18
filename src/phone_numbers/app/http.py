import logging
import json

import typing

from flask import Flask, jsonify, request, Response
from raven import Client  # type: ignore
from raven.contrib.flask import Sentry  # type: ignore
from raven.transport.requests import RequestsHTTPTransport  # type: ignore

from phone_numbers.lib.sentence_creator_fast import make_sentence_from_numbers
from phone_numbers.lib.trie import Trie
from phone_numbers.app.service_context import service_context


app = Flask(__name__)
sentry = Sentry(app, client=Client(transport=RequestsHTTPTransport,),)
logger = logging.getLogger(__name__)


def get_trie() -> Trie:
    with open("/usr/share/dict/words") as fh:
        words = [word.strip() for word in fh.readlines()]

    return Trie(words)


trie = service_context.clients.s3.get_or_create_file(
    "qsweber-temp", "phone-numbers/trie-extended", get_trie
)


@app.route("/api/v0/status", methods=["GET"])
def status() -> Response:
    logger.info("recieved request with args {}".format(json.dumps(request.args)))

    response = jsonify({"text": "ok"})
    response.headers.add("Access-Control-Allow-Origin", "*")

    return typing.cast(Response, response)


@app.route("/api/v0/match", methods=["GET"])
def match() -> Response:
    input_phone_number = request.args["value"]
    result = make_sentence_from_numbers(trie, input_phone_number)

    response = jsonify({"input": input_phone_number, "match": result})
    response.headers.add("Access-Control-Allow-Origin", "*")

    return typing.cast(Response, response)
