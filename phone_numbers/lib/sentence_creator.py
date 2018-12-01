import itertools
import re
from typing import List

from phone_numbers.lib.trie import Trie

LETTERS_BY_NUMBER = {
    2: ['a', 'b', 'c'],
    3: ['d', 'e', 'f'],
    4: ['g', 'h', 'i'],
    5: ['j', 'k', 'l'],
    6: ['m', 'n', 'o'],
    7: ['p', 'r', 's'],
    8: ['t', 'u', 'v'],
    9: ['w', 'x', 'y'],
}

NUMBER_BY_LETTER = {
    letter: number
    for number, letters in LETTERS_BY_NUMBER.items()
    for letter in letters
}


def make_sentence_from_string(trie: Trie, string: str, starting_index: int = 0) -> List[str]:
    '''
    Greedily creates words from an input string.

    For example, 'thisisworking' -> ['this', 'is', 'working']
    '''
    if not string:
        return []

    words: List[str] = []
    words2: List[str] = []
    longest_word = None
    word = []
    current = trie.trie

    reached_end = False
    i = starting_index
    max_i = len(string) - 1
    while True:
        letter = string[i]

        word.append(letter)

        if (letter in current and current[letter].is_word) or len(word) == 1:
            longest_word = ''.join(word)
            longest_word_index = i

        if (letter in current and (string[i + 1] if i < max_i else None in current[letter].children)):
            current = current[letter].children
            i = i + 1
        else:
            if not reached_end:
                words.append(longest_word)
            else:
                words2.append(longest_word)
            word = []
            i = longest_word_index + 1
            current = trie.trie

            if i == len(string):
                reached_end = True
                i = 0
                max_i = starting_index - 1

        if reached_end and i == starting_index:
            break

    return words2 + words


def make_sentence_from_string_non_greedy(trie: Trie, string: str) -> List[list]:
    return [
        make_sentence_from_string(trie, string, i)
        for i in range(len(string))
    ]


def get_best_option(trie: Trie, all_combinations: List[tuple]) -> List[str]:
    best_option: List[str] = []
    best_score = 0
    for possible in list(all_combinations):
        for i in range(len(possible)):
            sentence = make_sentence_from_string(trie, ''.join(possible), i)
            # score = len(max(words, key=lambda x: len(x))) # + len(possible) - len(words)
            # score = sum([
            #     1 if len(word) <= 2 else len(word) * (len(word) - 2)
            #     for word in words
            # ])
            score = len(possible) - len(sentence)
            if not best_option or score > best_score:
                best_option = sentence
                best_score = score

    return best_option


def cleanup_sentence(words: List[str]) -> str:
    if not words:
        return ''

    new_words = []
    consecutive_numbers = []
    for word in words:
        if len(word) == 1:
            consecutive_numbers.append(str(NUMBER_BY_LETTER.get(word, word)))
        else:
            if consecutive_numbers:
                new_words.append(''.join(consecutive_numbers))
                consecutive_numbers = []
            new_words.append(word)

    if consecutive_numbers:
        new_words.append(''.join(consecutive_numbers))

    return(' '.join(new_words))


def _clean_numbers(numbers: str) -> str:
    return re.sub(r'\D', '', ''.join(numbers))


def make_sentence_from_numbers(trie: Trie, numbers: str) -> str:
    cleaned_numbers = _clean_numbers(numbers)

    numbers_as_letters = [
        LETTERS_BY_NUMBER.get(int(number), str(number))
        for number in cleaned_numbers
    ]

    all_combinations: List[tuple] = list(itertools.product(*numbers_as_letters))

    best_option = get_best_option(trie, all_combinations)

    return cleanup_sentence(best_option)
