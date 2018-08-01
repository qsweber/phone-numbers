import random
import string

import pytest

from phone_numbers.words import WORDS
from phone_numbers.lib.words import get_new_words
from phone_numbers.lib.trie import Trie
from phone_numbers.lib import sentence_creator as module


trie = Trie(WORDS)
trie_new = Trie(get_new_words(WORDS))


@pytest.mark.parametrize(
    'string, expected',
    [
        ('thisisworking', ['this', 'is', 'working']),
        ('nominating', ['nominating']),
        ('12345', ['1', '2', '3', '4', '5']),
        ('test123test123', ['test', '1', '2', '3', 'test', '1', '2', '3']),
    ],
)
def test_make_sentence_from_string(string, expected):
    actual = module.make_sentence_from_string(trie, string)

    assert actual == expected


@pytest.mark.parametrize(
    'string, expected',
    [
        ('2679809273', 'copy 80 ward'),
        ('0003313039', '00033130 ex'),
        ('0000000000', '0000000000'),
        ('1800837863', '1800 test me'),
        ('abc1(800)-837-863', '1800 test me'),
        ('abcdef', ''),
    ],
)
def test_make_sentence_from_numbers(string, expected):
    actual = module.make_sentence_from_numbers(trie, string)

    assert actual == expected


@pytest.mark.parametrize(
    'string, expected',
    [
        ('2679809273', 'copy t0ward'),
        ('0003313039', '00 0dd 1d 0 ex'),
        ('0000000000', '0000000000'),
        ('1800837863', '1t 0 0vert me'),
    ],
)
def test_make_sentence_from_numbers_trie_new(string, expected):
    actual = module.make_sentence_from_numbers(trie_new, string)

    assert actual == expected


def test_never_errors():
    for i in range(10):
        random_numbers_as_string = ''.join(random.choices(list(string.digits), k=10))
        actual = module.make_sentence_from_numbers(trie, random_numbers_as_string)
        assert len(actual) >= len(random_numbers_as_string)
