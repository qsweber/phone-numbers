import itertools


def get_new_words(words):
    new_words = []
    for word in words:
        # 'food' should become 'f0od', 'f00d', 'fo0d'
        new_words.append(word)

        combinations = []
        indices_of_o_and_i = [pos for pos, char in enumerate(word) if char.lower() == 'o' or char.lower() == 'i']
        for r in list(range(1, len(indices_of_o_and_i) + 1)):
            combinations += list(itertools.combinations(indices_of_o_and_i, r))

        for combination in combinations:
            word_as_list = list(word)
            for index in combination:
                if word_as_list[index] == 'o':
                    word_as_list[index] = '0'
                elif word_as_list[index] == 'i':
                    word_as_list[index] = '1'

            new_words.append(''.join(word_as_list))

    return new_words
