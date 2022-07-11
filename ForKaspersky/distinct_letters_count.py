"""
2. DistinctLettersCount

Count the minimum number of letters that must be deleted from a word to create a word in which
no two letters occur the same number of times.

Task description
    Write a function: def solution(S)
    that, given a string S consisting of N lowercase letters, returns the minimum number of letters that must be deleted
    to obtain a word in which every letter occurs a unique number of times. We only care about occurrences of letters
    that appear at least once in result.
Examples:
    1. Given S = "aaaabbbb", the function should return 1. We can delete one occurrence of a or one occurrence of b.
        Then one letter will occur four times and the other one three times.
    2. Given S = "ccaaffddecee", the function should return 6. For example, we can delete all occurrences of e and f
        and one occurrence of d to obtain the word "ccaadc". Note that both e and f will occur zero times in the
        new word, but that is fine, since we only care about letters that appear at least once.
    3. Given S = "eeee", the function should return 0 (there is no need to delete any characters).
    4. Given S = "example", the function should return 4.
Write an efficient algorithm for the following assumptions:
    N is an integer within the range [0..300,000];
    string S consists only of lowercase letters (a−z).
"""
import logging
import sys
from collections import Counter

MAX_OCCURRENCE_COUNT = 300_000
VERBOSE = True


def solution(s: str) -> int:
    counter = Counter(s)
    logging.debug(counter)

    lowest_occurrence = MAX_OCCURRENCE_COUNT
    letters_to_delete_count = 0

    for letter, count in counter.most_common():
        logging.debug(f'"{letter}" x {count}')
        logging.debug(f'    {lowest_occurrence=}')

        if lowest_occurrence == 0:
            logging.debug(f'    Delete all ({count}) letters "{letter}"')
            letters_to_delete_count += count

        elif count < lowest_occurrence:
            lowest_occurrence = count
            logging.debug(f'    New lowest_occurrence = {lowest_occurrence}')

        else:
            lowest_occurrence -= 1
            logging.debug(f'    New lowest_occurrence = {lowest_occurrence}')
            delete_this_letter_count = count - lowest_occurrence
            letters_to_delete_count += delete_this_letter_count
            logging.debug(f'    {delete_this_letter_count} x "{letter}" to be deleted')

    logging.debug(f'{letters_to_delete_count=}')

    return letters_to_delete_count


if __name__ == '__main__':
    fmt = '%(levelname)-8s %(message)s'
    logging.basicConfig(level=logging.DEBUG if VERBOSE else logging.INFO, stream=sys.stdout, format=fmt)

    for sample in (
            'aaaaaaaabbbbbccccddddeeeeffffgggghhhiiijj',
            'AABcdefghi',
            '',
            'aaaabbbb',
            'ccaaffddecee',
            'eeee',
            'example',
    ):
        logging.info(f'Number of letters to be deleted: {solution(sample)}, string: "{sample}"')
