"CLI SPELL CHECKER"

# pip install python-Levenshtein~=0.12
# pip install numpy

import logging
import os

import Levenshtein
import numpy as np

DEFAULT_WORDS = "/usr/share/dict/words"
CUSTOM_WORDS = ""
LOG_FILENAME = f"{os.path.expanduser('~')}/spelling_log.txt"
LOGGING_ENABLED = True
# logging.basicConfig(format='%(asctime)s,%(message)s', datefmt='%d-%b-%y@%H:%M:%S', filename=LOG_FILENAME, level=logging.INFO)
if LOGGING_ENABLED:
    logging.basicConfig(format='%(asctime)s,%(message)s', datefmt='%Y-%m-%dT%H:%M:%S', filename=LOG_FILENAME, level=logging.INFO)

# Add this to your bashrc with the version of python you use and the path to this file.
# alias spell="python3 ~/spell.py" #> or where you placed this file.


""" EXAMPLES
$ spell honey
CORRECT: honey

$ spell pancreis
INCORRECT: pancreis
 - pancreas                                0.89
 - pancreatic                              0.73
 - pancreases                              0.73
 - pancreas's                              0.73
 - pantheist                               0.70
 - pantheism                               0.70
 - panderers                               0.70
 - pancake's                               0.70

$ spell test your spelling of words you mispelt
CORRECT: test
CORRECT: your
CORRECT: spelling
CORRECT: of
CORRECT: words
CORRECT: you
INCORRECT: mispelt
 - misspelt                                0.89
 - misspent                                0.78
 - misspell                                0.78
 - misdealt                                0.78
 - respelt                                 0.75
 - dispels                                 0.75
 - spelt                                   0.71
 - dispel                                  0.71


$ spell I have been raking my brain all day about learn algera
CORRECT: i
CORRECT: have
CORRECT: been
CORRECT: raking
CORRECT: my
CORRECT: brain
CORRECT: all
CORRECT: day
CORRECT: about
CORRECT: learn
INCORRECT: algera
 - algebra                                 0.88
 - algebras                                0.78
 - Algeria                                 0.75
 - augers                                  0.71
 - angora                                  0.71
 - angers                                  0.71
 - alters                                  0.71
 - alders                                  0.71


$ spell test your spelling of words you mispelt --fix
CORRECT: test
CORRECT: your
CORRECT: spelling
CORRECT: of
CORRECT: words
CORRECT: you
INCORRECT: mispelt
 - misspelt                                0.89
 - misspent                                0.78
 - misspell                                0.78
 - misdealt                                0.78
 - respelt                                 0.75
 - dispels                                 0.75
 - spelt                                   0.71
 - dispel                                  0.71
 
AUTOCORRECT: test your spelling of words you misspelt

"""




# Default words list on linux: 102,306 words on ubuntu
with open(DEFAULT_WORDS, "r") as f: #> "/usr/share/dict/words"
    words = f.readlines()
    
## Uncomment to add a path to custom words a word list
if CUSTOM_WORDS:
    with open(CUSTOM_WORDS, "r") as f:
        customs_words = f.readlines()
    words = words + customs_words


# print(len(words))

# convert input strings to NumPy matrices, would be nice to cache this.
len_to_words = {}
for w in words: 
    len_to_words.setdefault(len(w), []).append(w.rstrip('\n'))

# Add a faster way to do this
len_to_mat2 = {n: np.asarray([[ord(c) for c in w] for w in ws], dtype=np.uint16).T
              for n, ws in len_to_words.items()}


def levenshtein_distance_vec(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """
    """
    m, n, k = len(a), len(b), b.shape[1]
    d = np.zeros((m+1, n+1, k), dtype=np.uint16)  # d[i,j] = levenshtein_distance(a[:i], b[:j])

    # when the other string is empty, distance is length of non-empty string
    for i in range(m+1): d[i, 0] = i
    for i in range(n+1): d[0, i] = i
    
    for j in range(1, n+1):
        for i in range(1, m+1):
            cost = a[i-1] != b[j-1]
            d[i, j] = np.min([d[i-1, j-1] + cost,        # substitute         ↘
                              d[i, j-1]   + 1,           # delete from B      →
                              d[i-1, j]   + 1], axis=0)  # insert into B      ↓

    return d[m, n]


def interact_words_levenshtein_vec(input_text, private=False):
    """
    """
    a_vec = np.asarray([ord(c) for c in input_text])
    n = len(input_text)
    xs, ys = [], []
    
    for m, b_mat in len_to_mat2.items():
        if abs(m - n) > 5: continue  # 🔧 again, skipping strings with obvious large distance
        dist = levenshtein_distance_vec(a_vec, b_mat)
        # dist = levenshtein_distance_vec(a_vec, b_mat)
        scores = 1.0 - dist/max(n, m)
        xs.extend(len_to_words[m])
        ys.extend(scores) 
    
    if not input_text: return
    i = 1

    top_results = list(sorted(zip(ys, xs), reverse=True))[:8]
    if int(top_results[0][0]) == 1:
        print(f"CORRECT: {input_text}")
        return input_text
    print(f"INCORRECT: {input_text}")
    for score, word in top_results:
        # print(f"{i}\t{word:40}{score:3.2f}")
        print(f" - {word:40}{score:3.2f}")
        i += 1
    print(" ")

    top_guess = top_results[0][1]
    top_score = round(top_results[0][0], 2)
    if private is False:
        logging.info(f'{input_text},{top_guess},{top_score}')
    return top_guess


    # input("Enter another word")

    # import pyperclip
    # pyperclip.copy('The text to be copied to the clipboard.')

# widgets.interact(interact_words_levenshtein_vec, input_text="");


if __name__ == '__main__':
    import sys

    corrected = []
    args = sys.argv

    fix_flag = "--fix" in set(args)
    disable_log = "--private" in set(args)

    del args[0]
    # print(input_text)
    for input_text in [e for e in args if not e.startswith("--")]:
        top_guess = interact_words_levenshtein_vec(input_text.lower().strip(), private=disable_log)
        corrected.append(top_guess)

    if fix_flag:
        print("AUTOCORRECT: "+ ' '.join(corrected))

    if disable_log:
        print("PRIVATE MODE: True")
    
    """
    TODO:
    
    - Would be nice to save the history, so you can learn
    - Add new words
    - Tell it which word was the correct one
    - Cache the word list vectors
    - copy the correct spelling to the clipboard
    - Select key pad on word to see definition
    - Show colour diff of the words to show you what letter you missed
    - Use phonic search if you cant find it
    - Select key pad on word to see words with similar meanings
    - Game to test your spelling of words you misspelt in the past
    - hard mode - ask you to retype it correctly to leave the screen - and copies it to clipboard
    - Use colour to make it easier to read
    - real time search
    - search another word
    """


