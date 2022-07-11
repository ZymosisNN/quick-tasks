"""
1. OddWord

Find a string of a given length such that each letter occurs an odd number of times.

Task description
    Write a function solution that, given an integer N, returns a string consisting of N lowercase letters (a−z)
    such that each letter occurs an odd number of times. We only care about occurrences of letters that appear
    at least once in the result.
Examples:
    1. Given N = 4, the function may return "code" (each of the letters "c", "o", "d" and "e" occurs once).
        Other correct answers are: "cats", "uutu" or "xxxy".
    2. Given N = 7, the function may return "gwgtgww" ("g" and "w" occur three times each and "t" occurs once).
    3. Given N = 1, the function may return "z".
Write an efficient algorithm for the following assumptions:
    N is an integer within the range [1..200,000].
"""


def solution(n: int) -> str:
    assert 0 < n < 200_000
    if n % 2 == 0:
        return 'a' * (n - 1) + 'b'
    else:
        return 'a' * n


if __name__ == '__main__':
    for i in (4, 7, 1, 26, 36):
        print(f'{i:3d}, string: "{solution(i)}"')
