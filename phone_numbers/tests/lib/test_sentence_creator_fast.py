import random
import string

import pytest

from phone_numbers.lib.trie import Trie
from phone_numbers.lib import sentence_creator_fast as module


with open('/usr/share/dict/words') as fh:
    words = [
        word.strip()
        for word in fh.readlines()
    ]

trie = Trie(words)


@pytest.mark.parametrize(
    'string, expected',
    [
        ('2679809273', 'copy 80 ward'),
        ('0000000000', '0000000000'),
        ('1800837863', '1800 test me'),
        ('abc1(800)-837-863', '1800 test me'),
        ('abcdef', ''),
        ('22738275', 'aardvark'),
        ('2273827522738275', 'aardvark aardvark'),
        ('227382758322738275', 'aardvark te aardvark'),  # notice how it doesn't do "aardvark tea ..."
    ],
)
def test_make_sentence_from_numbers(string, expected):
    actual = module.make_sentence_from_numbers(trie, string)

    assert actual == expected


def test_never_errors():
    for i in range(10):
        random_numbers_as_string = ''.join(random.choices(list(string.digits), k=10))
        actual = module.make_sentence_from_numbers(trie, random_numbers_as_string)
        assert len(actual) >= len(random_numbers_as_string)
