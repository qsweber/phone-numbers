import re
from typing import Dict, List, Tuple

from phone_numbers.lib.trie import Trie, _Element


LETTERS_BY_NUMBER = {
    2: ["a", "b", "c"],
    3: ["d", "e", "f"],
    4: ["g", "h", "i"],
    5: ["j", "k", "l"],
    6: ["m", "n", "o"],
    7: ["p", "r", "s"],
    8: ["t", "u", "v"],
    9: ["w", "x", "y"],
}


def find_longest_word(
    mapping: Dict[str, _Element],
    letter_options: List[Tuple[str, List[str]]],
    word_so_far: str,
    valid_word_so_far: str,
) -> str:
    if not letter_options:
        return valid_word_so_far

    results: List[str] = []
    for next_letter in letter_options[0][1]:
        if next_letter in mapping:
            results.append(
                find_longest_word(
                    mapping[next_letter].children,
                    letter_options[1:],
                    word_so_far + next_letter,
                    word_so_far + next_letter
                    if mapping[next_letter].is_word
                    else valid_word_so_far,
                )
            )

    if not results:
        return valid_word_so_far

    return max(results, key=len)


def find_collection_of_longest_words(
    trie: Trie, letter_options: List[Tuple[str, List[str]]],
) -> List[str]:
    if not letter_options:
        return []

    best_longest_word = ""
    best_starting_index = 0
    for starting_index in range(len(letter_options)):
        longest_word = find_longest_word(
            trie.root, letter_options[starting_index:], "", ""
        )

        if not longest_word or len(longest_word) == 1:
            longest_word = letter_options[starting_index][0]

        if not best_longest_word or len(longest_word) > len(best_longest_word):
            best_longest_word = longest_word
            best_starting_index = starting_index

    result = [best_longest_word]

    leftover_before = letter_options[0:best_starting_index]
    leftover_after = letter_options[(best_starting_index + len(best_longest_word)) :]

    if leftover_before:
        result = find_collection_of_longest_words(trie, leftover_before) + result

    if leftover_after:
        result = result + find_collection_of_longest_words(trie, leftover_after)

    return result


def clean_input(number: str) -> str:
    return re.sub(r"\D", "", "".join(number))


def make_sentence_from_numbers(trie: Trie, number: str) -> str:
    cleaned_number = clean_input(number)

    letter_options = [
        (
            str(n),
            LETTERS_BY_NUMBER[int(n)]
            if n.isdigit() and int(n) in LETTERS_BY_NUMBER
            else [str(n)],
        )
        for n in cleaned_number
    ]

    result = find_collection_of_longest_words(trie, letter_options)

    sentence = ""
    last_is_digit = False
    for word in result:
        if sentence and not (last_is_digit and word.isdigit()):
            sentence += " "

        sentence += word

        last_is_digit = word.isdigit()

    return sentence
