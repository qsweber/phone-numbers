import itertools
import re


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


def make_sentence_from_string(trie, string):
    '''
    Greedily creates words from an input string.

    For example, 'thisisworking' -> ['this', 'is', 'working']
    '''
    words = []
    longest_word = None
    word = []
    current = trie.trie
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
            current = trie.trie

    return words


def get_best_option(trie, all_combinations):
    best_option = None
    best_score = 0
    for possible in list(all_combinations):
        words = make_sentence_from_string(trie, ''.join(possible))
        # score = len(max(words, key=lambda x: len(x))) # + len(possible) - len(words)
        # score = sum([
        #     1 if len(word) <= 2 else len(word) * (len(word) - 2)
        #     for word in words
        # ])
        score = len(possible) - len(words)
        if not best_option or score > best_score:
            best_option = words
            best_score = score

    return best_option


def cleanup_sentence(words):
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


def clean_numbers(numbers):
    return re.sub("\D", "", ''.join(numbers))


def make_sentence_from_numbers(trie, numbers):
    cleaned_numbers = clean_numbers(numbers)

    numbers_as_letters = [
        LETTERS_BY_NUMBER.get(int(number), str(number))
        for number in cleaned_numbers
    ]

    all_combinations = itertools.product(*numbers_as_letters)

    best_option = get_best_option(trie, all_combinations)

    return cleanup_sentence(best_option)
