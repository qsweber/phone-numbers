import itertools


class Element:
    def __init__(self, is_word=False):
        self.is_word = is_word
        self.children = {}


class Trie:
    def __init__(self, words):
        trie = {}
        for word in words:
            trie = self.add_word_to_trie(trie, word)
        self.trie = trie

    def add_word_to_trie(self, trie, word):
        current = trie
        for index, letter in enumerate(word):
            if index == len(word) - 1:
                if letter in current:
                    current[letter].is_word = True
                else:
                    current[letter] = Element(is_word=True)
            else:
                if letter not in current:
                    current[letter] = Element()

                current = current[letter].children

        return trie

    def make_sentence_from_string(self, string):
        words = []
        longest_word = None
        word = []
        current = self.trie
        i = 0
        while i < len(string):
            letter = string[i]

            word.append(letter)

            if (letter in current and current[letter].is_word) or len(word) == 1:
                longest_word = ''.join(word)
                longest_word_index = i

            if (letter in current and (string[i + 1] if i < len(string) - 1 else None in current[letter].children)):
                current = current[letter].children
                i = i + 1
            else:
                words.append(longest_word)
                word = []
                i = longest_word_index + 1
                current = self.trie

        return words

    def make_sentence_from_numbers(self, string):
        numbers_to_letters = {
            2: ['a', 'b', 'c'],
            3: ['d', 'e', 'f'],
            4: ['g', 'h', 'i'],
            5: ['j', 'k', 'l'],
            6: ['m', 'n', 'o'],
            7: ['p', 'r', 's'],
            8: ['t', 'u', 'v'],
            9: ['w', 'x', 'y'],
        }

        letters_to_numbers = {}
        for n, ls in numbers_to_letters.items():
            for l in ls:
                letters_to_numbers[l] = n

        phone_number_as_letters = [
            numbers_to_letters.get(int(number), number)
            for number in string
        ]

        best_option = None
        for possible in list(itertools.product(*phone_number_as_letters)):
            option = self.make_sentence_from_string(''.join(possible))
            if not best_option or len(option) < len(best_option):
                best_option = option
                foo = possible

        best_option = [
            word if isinstance(word, str) and len(word) > 1 else int(letters_to_numbers.get(word, word))
            for word in best_option
        ]

        new_words = []
        foo = []
        for word in best_option:
            if isinstance(word, str):
                if foo:
                    new_words.append(''.join(foo))
                    foo = []
                new_words.append(word)
            else:
                foo.append(str(word))

        if foo:
            new_words.append(''.join(foo))

        return(' '.join(new_words))
