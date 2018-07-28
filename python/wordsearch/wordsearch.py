#!/usr/bin/env python3

import random
import string
import argparse
import sys


def read_solutions(filename):
    """
    Read filename with vocabulary to a list.
    """
    with open(filename, "r") as f:
        return [line.replace('\n', '').upper() for line in f]


def generate_board(size):
    """
    Rectangle board generating
    """
    generated_list = []
    for i in range(size):
        a = ''.join(random.choices(string.ascii_uppercase, k=size))
        generated_list.append(a + '\n')
    all_in_one_string = ''.join([line for line in generated_list])[:-1]
    return all_in_one_string


def create_list(wordgrid):
    """
    Create all posible values from wordboard according to game rules.
    """
    # Horizontal length of table
    length = wordgrid.index('\n') + 1

    # Enumerate creates a list of tuples [(0, 'B'), (1, 'P'),...]
    # Tuple and Divmod in fact creates smth like coordinates of each letter.
    # [('B', (0, 0)), ('P', (0, 1)),...]
    characters = []
    for index, letter in enumerate(wordgrid):
        characters.append(tuple([letter, divmod(index, length)]))

    wordlines = {}

    # Offsets for 3 directions
    directions = {'⇓': 0,
                  '⇙': -1,
                  '⇘': 1}

    # Getting all possible combinations in ⇓, ⇙, ⇘ directions
    for symbol_direction, offset in directions.items():
        wordlines[symbol_direction] = []

        for x in range(length):
            for i in range(x, len(characters), length + offset):
                wordlines[symbol_direction].append(characters[i])
            wordlines[symbol_direction].append('\n')

    # Getting all possible combinations in ⇒, ⇐, ⇑, ⇖, ⇗ directions
    wordlines['⇒'] = characters
    wordlines['⇐'] = list(reversed(characters))
    wordlines['⇑'] = list(reversed(wordlines['⇓']))
    wordlines['⇖'] = list(reversed(wordlines['⇘']))
    wordlines['⇗'] = list(reversed(wordlines['⇙']))
    return wordlines


def search_words(lines, solutions):
    """
    Looking for matches in wordboard and vocabulary
    """
    for symbol_offset, tuple in lines.items():
        string = ''.join([i[0] for i in tuple])
        for word in solutions:
            if word in string:
                coordinates = tuple[string.index(word)][1]
                print("{} starting at row {} and column {} {}".
                      format(word,
                             coordinates[0]+1,
                             coordinates[1]+1,
                             symbol_offset))


def main():
    """
    Main logic
    """
    if len(sys.argv) > 1:
        pass
    else:
        print("Needed -s (--size) parameter")
        sys.exit(1)

    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument('-s', '--size', type=int, dest="size",
                        help="board size")
    args = parser.parse_args()

    wordgrid = generate_board(args.size)
    print('** This is GAMEBOARD **')
    print(wordgrid)
    print('*' * 22)

    solutions = read_solutions("words.txt")
    wordlines = create_list(wordgrid)
    search_words(wordlines, solutions)


if __name__ == "__main__":
    main()
