import pytest

from phone_numbers.words import WORDS
from phone_numbers.lib import trie as module


@pytest.mark.parametrize(
    'string, expected',
    [
        ('thisisworking', ['this', 'is', 'working']),
    ],
)
def test_make_sentence_from_string(string, expected):
    trie = module.Trie(WORDS)

    actual = trie.make_sentence_from_string(string)

    assert actual == expected


@pytest.mark.parametrize(
    'string, expected',
    [
        ('2679809273', 'copy 80 ward'),
        ('0003313039', '00033130 ex')
    ],
)
def test_make_sentence_from_numbers(string, expected):
    trie = module.Trie(WORDS)

    actual = trie.make_sentence_from_numbers(string)

    assert actual == expected
