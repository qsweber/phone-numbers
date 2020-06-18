import typing


class _Element:
    def __init__(self, is_word: bool = False) -> None:
        self.is_word = is_word
        self.children: typing.Dict[str, _Element] = {}


class Trie:
    def __init__(self, words: typing.List[str]) -> None:
        trie: typing.Dict[str, _Element] = {}
        for word in words:
            trie = self._add_word_to_trie(trie, word)

        self.root = trie

    def _add_word_to_trie(
        self, trie: typing.Dict[str, _Element], word: str
    ) -> typing.Dict[str, _Element]:
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
