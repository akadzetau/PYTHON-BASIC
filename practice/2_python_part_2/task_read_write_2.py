"""
Use function 'generate_words' to generate random words.
Write them to a new file encoded in UTF-8. Separator - '\n'.
Write second file encoded in CP1252, reverse words order. Separator - ','.

Example:
    Input: ['abc', 'def', 'xyz']

    Output:
        file1.txt (content: "abc\ndef\nxyz", encoding: UTF-8)
        file2.txt (content: "xyz,def,abc", encoding: CP1252)
"""


def generate_words(n=20):
    import string
    import random

    words = list()
    for _ in range(n):
        word = ''.join(random.choices(string.ascii_lowercase, k=random.randint(3, 10)))
        words.append(word)

    return words


def write_n(file: str, wrds: list):
    with open(file, 'w', encoding='UTF-8') as f1:
        f1.write("\n".join(wrds))


def write_rev_sep(file: str, wrds: list):
    wrds.reverse()
    with open(file, 'w', encoding='CP1252') as f1:
        f1.write(",".join(wrds))


if __name__ == "__main__":
    rnd_words = generate_words(20)
    write_n('file1.txt', rnd_words)
    write_rev_sep('file2.txt', rnd_words)