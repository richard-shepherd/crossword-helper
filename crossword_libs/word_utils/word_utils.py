import itertools


class WordUtils(object):
    """
    Utility functions for working with words.
    """

    @staticmethod
    def remove_letters_from_word(word, letters):
        """
        Removes letters from word. 

        NOTE 1: Only one of each letter is removed. For example, ("hello", "l") -> "helo"
        NOTE 2: letters can be a string or a collection of individual letters
        """
        result = word
        for letter in letters:
            result = result.replace(letter, "", 1)
        return result

    @staticmethod
    def letter_combinations(word, lengths):
        """
        Returns an iterable for combinations of letters in the word requested
        with the lengths requested. For example:
          letter_combinations("abcd", [1, 3] -> ("a", "bcd"), ("b", "acd"), ...
        """

        num_lengths = len(lengths)
        if num_lengths == 1:
            # We only have one length, so we return the combinations of words of that length...
            length = lengths[0]
            unique_words = set()

            # We loop through the combinations of words with length letters...
            combinations = itertools.combinations(word, length)
            for combination in combinations:
                # If the word is not one we've seen before, we return it.
                # NOTE: This is done as combinations are unique on the position of letters
                #       not on their value. So combinations of "hello" for example otherwise 
                #       include "hel" twice, once for each l in the word.
                word_with_length = "".join(combination)
                if word_with_length in unique_words: continue
                unique_words.add(word_with_length)
                yield [word_with_length]
        else:
            # We have more than one length.

            # We first find combinations of letters with the first length...
            combinations_with_first_length = WordUtils.letter_combinations(word, lengths[:1])

            # For each of these combinations of letters, we find the remaining letters
            # from the original word when they are removed, and then break these down
            # by the next letter-lengths...
            unique_remaining_letters = set()
            for combination_with_first_length in combinations_with_first_length:
                # Each combination is returned as a list. We find the word from the list, and
                # then find the remaining letters...
                word_with_first_length = combination_with_first_length[0]
                remaining_letters = WordUtils.remove_letters_from_word(word, word_with_first_length)
                if remaining_letters in unique_remaining_letters: continue
                unique_remaining_letters.add(remaining_letters)

                # We find the combinations of the remaining letters broken down by the remaining lengths...
                remaining_combinations = WordUtils.letter_combinations(remaining_letters, lengths[1:])

                # We return each original combination, along with the combinations of the remainder...
                for remaining_combination in remaining_combinations:
                    l = list(combination_with_first_length)
                    l.extend(remaining_combination)
                    yield l

