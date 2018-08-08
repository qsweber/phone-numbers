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
    'string, starting_index, expected',
    [
        ('thisisworking', 0, ['this', 'is', 'working']),
        ('nominating', 0, ['nominating']),
        ('12345', 0, ['1', '2', '3', '4', '5']),
        ('test123test123', 0, ['test', '1', '2', '3', 'test', '1', '2', '3']),
        ('thenewt', 0, ['then', 'e', 'w', 't']),  # greedy
        ('thenewt', 3, ['the', 'newt']),  # not greedy
    ],
)
def test_make_sentence_from_string(string, starting_index, expected):
    actual = module.make_sentence_from_string(trie, string, starting_index)

    assert actual == expected


def test_make_sentence_from_string_non_greedy():
    actual = module.make_sentence_from_string_non_greedy(trie, 'thenewt')

    assert actual == [
        ['then', 'e', 'w', 't'],
        ['t', 'hen', 'e', 'w', 't'],
        ['t', 'h', 'e', 'newt'],
        ['the', 'newt'],
        ['then', 'e', 'w', 't'],
        ['then', 'e', 'w', 't'],
        ['then', 'e', 'w', 't'],
    ]


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
        ('0003313039', '00 0dd 1 d0e 9'),
        ('0000000000', '0000000000'),
        ('1800837863', '1 t00t drum 3'),
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
