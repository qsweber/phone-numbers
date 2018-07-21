import phone_numbers.lib.words as module

import pytest


@pytest.mark.parametrize(
    'words, expected',
    [
        (['food'], ['food', 'f0od', 'fo0d', 'f00d']),
        (['riot'], ['riot', 'r1ot', 'ri0t', 'r10t']),
    ],
)
def test_make_sentence_from_string(words, expected):
    actual = module.get_new_words(words)

    assert actual == expected
