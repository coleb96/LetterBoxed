import datetime
import os
import sys
import pprint
import urllib.request, json

DICTIONARY_URL = (
    r"https://raw.githubusercontent.com/dwyl/english-words/master/words_dictionary.json"
)
DICTIONARY_LOCAL_FILE = "words_today.json"

def download_words(should_cache: bool) -> dict:
    if os.path.isfile(DICTIONARY_LOCAL_FILE):
        with open(DICTIONARY_LOCAL_FILE, "r") as file_handle:
            data: dict = json.load(file_handle)
        return data

    with urllib.request.urlopen(DICTIONARY_URL) as url:
        data: dict = json.load(url)
    if should_cache:
        with open(DICTIONARY_LOCAL_FILE, "w") as file_handle:
            json.dump(data, file_handle)
    return data

"""
dfs returns the set of valid words able to be formed by the given box letters
"""
def dfs(i: int, j: int, box: list[list[str]], curr_word: str, trie: dict) -> set:
    if not prefix_in_trie(trie, curr_word):
        return set()

    result = set()
    if len(curr_word) > 2 and in_trie(trie, curr_word):
        result.add(curr_word)
    
    # explore each of the other letters not in this row
    for x in range(len(box)):
        if x == i:
            continue
        for y in range(len(box[0])):
            result = result | dfs(x, y, box, curr_word + box[x][y], trie)
    return result

"""
solve determines the optimal solutions for the given letter box based on
the valid word set in the trie.

it solves it by first using DFS + backtracking to determine the valid words
formed by the box. then it checks each of those valid words, again with DFS,
by picking words where the last letter is equal to the next letter in each
recursive call.

it assumes that it will find a solution that is at least 5 words in length
and starts from the bottom (checking any 1 word solutions) and goes up
from there.

it will stop searching when a list of solutions of some length has been found
(usually 2).
"""
def solve(box: list[list[str]], trie: dict) -> list[list[str]]:
    possible_words: set[str] = set()
    for i in range(len(box)):
        for j in range(len(box[0])):
            possible_words = possible_words | dfs(i, j, box, box[i][j], trie)
    
    # make map of first letter -> all possible words of that letter
    word_map: dict[str, list[str]] = dict()
    for k in possible_words:
        begin_letter = k[0]
        if begin_letter not in word_map:
            word_map[begin_letter] = []
        word_map[begin_letter].append(k)

    solutions = []
    solution_length, found = 1, False
    while solution_length < 5 and not found:
        for k in possible_words:
            solution_set = find_solutions(k, [k], word_map, box, solution_length)
            if len(solution_set) > 0:
                solutions += solution_set
                found = True
        solution_length += 1
    return solutions

"""
find_solutions will use DFS on the word_map to find possible solutions to the box.

the `word_map` must be a dictionary where the key is a letter and the value is a list of words
that start with that letter.
"""
def find_solutions(curr_word: str, word_list: list[str], word_map: dict[str, list[str]], box: list[list[str]], max_len: int) -> list[list[str]]:
    # print(f'curr_word: {curr_word}, word_list: {word_list}')
    # if it's a word, try adding it to the word list and see if it makes a solution
    if is_solution(word_list, box):
        return [word_list]

    if len(word_list) > max_len:
        return []

    next_letter = curr_word[-1]

    solutions = []
    for w in word_map[next_letter]:
        if w in word_list:
            continue
        solutions += find_solutions(w, word_list+[w], word_map, box, max_len)
    return solutions

def is_solution(words: list[str], box: list[list[str]]) -> bool:
    used_letters = "".join(words)
    for row in box:
        for l in row:
            if l not in used_letters:
                return False
    return True

_end = '_end_'

"""
make_trie returns a trie in the form of a nested dictionary
"""
def make_trie(words: list[str]) -> dict:
    root = dict()
    for word in words:
        current_dict = root
        for letter in word:
            current_dict = current_dict.setdefault(letter, {})
        current_dict[_end] = _end
    return root

"""
in_trie returns whether the word exists in the trie
"""
def in_trie(trie, word) -> bool:
    current_dict = trie
    for letter in word:
        if letter not in current_dict:
            return False
        current_dict = current_dict[letter]
    return _end in current_dict

"""
prefix_in_trie returns whether the string prefix is present in the trie
note: this will return True if the prefix also happens to be a word.
e.g. "program" is a prefix of "programming" but is also a word itself.
"""
def prefix_in_trie(trie, word):
    current_dict = trie
    for letter in word:
        if letter not in current_dict:
            return False
        current_dict = current_dict[letter]
    return True

if __name__ == "__main__":
    args = sys.argv[1:]
    should_cache = False
    if "-cache" in args:
        should_cache = True

    words: dict[str, int] = download_words(should_cache)
    t = make_trie([w.upper() for w in words.keys()])
    a = datetime.datetime.now()
    box = [
        ["A", "P", "L"],
        ["R", "U", "D"],
        ["N", "M", "G"],
        ["F", "I", "O"],
    ]
    solutions = solve(box, t)
    b = datetime.datetime.now()
    pprint.pprint(solutions, indent=2)
    print(f'found {len(solutions)}, {len(solutions[0])}-word solutions in {(b-a).microseconds / 1000.0 / 1000.0 } seconds')
