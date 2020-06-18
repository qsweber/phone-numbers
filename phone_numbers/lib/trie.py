
class _Element:
    def __init__(self, is_word=False):
        self.is_word = is_word
        self.children = {}


class Trie:
    def __init__(self, words):
        trie = {}
        for word in words:
            trie = self._add_word_to_trie(trie, word)

        self.root = trie

    def _add_word_to_trie(self, trie, word):
        current = trie
        for index, letter in enumerate(word):
            if index == len(word) - 1:
                if letter in current:
                    current[letter].is_word = True
                else:
                    current[letter] = _Element(is_word=True)
            else:
                if letter not in current:
                    current[letter] = _Element()

                current = current[letter].children

        return trie
