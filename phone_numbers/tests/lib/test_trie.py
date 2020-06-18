import pickle

from phone_numbers.lib.trie import Trie, _Element


def test_trie():
    words = ['foo', 'food', 'for']

    elementD = _Element(is_word=True)
    elementD.children = {}

    elementR = _Element(is_word=True)
    elementR.children = {}

    elementO2 = _Element(is_word=True)
    elementO2.children = {'d': elementD}

    elementO1 = _Element(is_word=False)
    elementO1.children = {'o': elementO2, 'r': elementR}

    elementF = _Element(is_word=False)
    elementF.children = {'o': elementO1}

    expected = {'f': elementF}

    actual = Trie(words)

    assert pickle.dumps(actual.root) == pickle.dumps(expected)
