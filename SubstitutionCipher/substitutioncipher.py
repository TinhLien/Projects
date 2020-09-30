# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from string import punctuation
from collections import Counter, defaultdict
from functools import lru_cache
import pickle
import time
import priority_queue


"""Please test this is in a fairly modern python version , as versions older than python 3.7 may cause errors with this program"""

"""NOTE : To test this program you must change line 231 with open(filename) to whatever the name of the file you are decrypting.It is set to cipher.txt as this was the 
default filename I used"""

"""Output of this program will be put into two differnt text files , one for the decrypted text and the other for the key"""

#case_sensitive paramater saves a lot of code and speeds it up
def translate(text, char_mapping, case_sensitive=False):
    if case_sensitive:
        char_mapping = char_mapping.copy()
        for k, v in char_mapping.copy().items():
            char_mapping[k.upper()] = v.upper()
    return text.translate(str.maketrans(char_mapping))


def match_pattern(cypher_word, word, char_mapping):
    "Check if cypher_word could translate into word using char_mapping"
    for cypher_letter, letter in zip(cypher_word, word):
        if cypher_letter in char_mapping:
            if char_mapping[cypher_letter] != letter:
                return False
    return True


def compare_partially_decrypted(crypted_word, word, char_mapping):
    """
    Compare crypted_word with word, only considering the letters
    which have a mapping in char_mapping
    """
    for cc, cw in zip(crypted_word, word):
        if cc in char_mapping and char_mapping[cc] != cw:
            return False
    return True


def get_score(cypher_words, char_mapping, words):
    """
    Compute a "score" for the char_mapping over the list of cypher_words

    For each word in the list of cypher_words, we will score points if the
    cypher_word could match a word from words by only looking at the letters
    in char_mapping.
    In other words if the cypher_word was "sif" and the char_mapping was
    {'s': 'd', 'f': 'g'}, the partial decyphering of "sif" would be "DiG".
    This could match "DoG" in the english dictionary so we can score 1 point.

    We score 0.5 points if the cypher_word could match anything, because none of
    its letters are in char_mapping
    If we can match one english word, we will score points in accordance with its
    frequency.
    """
    score = 0
    eng_chars = set(char_mapping.values())
    for cypher_word in cypher_words:
        cypher_pattern = make_pattern(cypher_word)
        decrypted_word = translate(cypher_word, char_mapping)
        if decrypted_word == cypher_word:
            # Nothing decrypted from this word. It could match anything!
            #This is the 1st case
            #Know nothing about the letters of the word so far , so we dont give it as much weight
            #We dont give negative scores , so this is sort of a "penalty" to be added to the score
            score += 0.5
            continue

        if set(cypher_word) <= char_mapping.keys():
            # All letters are decrypted. Is it in dictionary?
            if decrypted_word in set(words[cypher_pattern]):
                freq = words[cypher_pattern].index(decrypted_word)
                #This is the 2nd case
                # Add more weight to fully decyphered English words + their frequency
                # For 3 letters words, if there are 20 words in dictionary, the frequency score
                # is based on the formula (20 - position) / 20 => number between 0.0 and 1.0.
                score += 1 + 2*(len(words[cypher_pattern]) - freq) / len(words[cypher_pattern]) 
            continue

        for english_word in words[cypher_pattern]:
            #This is the 3rd case
            #You have a few letters of the word not all the letters , so you can partially decrypt it
            #We can now look at likely english words that could be a potential word , so more than likely we are on the right track
            #So theres 2 ways this could be wrong 1)The word is not in the Dictionary unfortunately 2)We are on the wrong track
            #There is less weight here for score as its partially decrypted
            if compare_partially_decrypted(cypher_word, english_word, char_mapping):
                freq = words[cypher_pattern].index(english_word)
                score += 1 + (len(words[cypher_pattern]) - freq) / len(words[cypher_pattern])
                break
    return score


@lru_cache()
#Because we are calling match_pattern a l, we put offer into memory to speed it up (memoization)
def make_pattern(word):
    """
    Create a tuple of integers representing the letters in word.

    Integers starts at 0 and in case of repetitive letters, the same
    integer is used.

    Eg.: 'offer'  ->  (0, 1, 1, 2, 3)
    """
    i = 0
    mapping = {}
    pattern = []
    for c in word:
        if c in mapping:
            pattern.append(mapping[c])
        else:
            pattern.append(i)
            mapping[c] = i
            i += 1
    return tuple(pattern)


def build_english_frequency_dictionary(filepath):
    """
    Build a dictionary of english words from a text file, grouping the words
    by their letters pattern, and sorting the words by the order they were read in
    the file.
    {word_pattern: [words sorted by frequency]}
    """
    words = defaultdict(list)
    with open(filepath) as f:
        for word in f.read().splitlines():
            words[make_pattern(word)].append(word)
            # 'all' -> {(0, 1, 1): ['all', 'off', ...]}

    # Open the file in write binary mode
    with open('dictionary.dat', 'wb') as f:
        pickle.dump(words, f)


def load_english_frequency_dictionary(filepath):
    """
    Loads the pickled dictionary of english words.

    See `build_english_frequency_dictionary` for more details.
    """
    with open(filepath, 'rb') as f:
        words = pickle.load(f)
    return words


def add_to_queue(char_mapping, cypher_index, priority):
    """
    Add to a priority queue our current char_mapping and cypher_index.

    Tha char_mapping cannot be stored directly in the priority queue. So
    we store the string of keys and values separately.
    """
    crypted_letters = "".join(char_mapping.keys())
    english_letters = "".join(char_mapping.values())
    priority_queue.add_task(
        (crypted_letters, english_letters, cypher_index, -priority),
        priority=priority
    )


def pop_from_queue():
    """
    Pop char_mapping and cypher_idx from priority queue.

    This function will reconstruct the char_mapping from the cypher_letters
    and english_letters
    """
    crypted_letters, english_letters, cypher_index, priority = priority_queue.pop_task()
    char_mapping = dict(zip(crypted_letters, english_letters))
    return char_mapping, cypher_index, priority


def decrypt(text):
    words = load_english_frequency_dictionary("dictionary.dat")
    cypher_words = ''.join(c for c in text if c not in punctuation).lower().split()
    cypher_words_counter = Counter(cypher_words)
    cypher_words = [cypher_word for cypher_word, freq in cypher_words_counter.most_common()]
    # Append to the pq the (char_mapping, cypher_index)
    # with priority of score
    add_to_queue({}, 0, priority=0)
    while True:
        char_mapping, cypher_index, current_score = pop_from_queue()
        if cypher_index >= len(cypher_words):
            # Did we find something??
            break

        cypher_word = cypher_words[cypher_index]
        # Get all the possible words of similar length which align with
        # the current char_mapping
        matches = [
            (idx, word) for (idx, word) in enumerate(words[make_pattern(cypher_word)])
            if match_pattern(cypher_word, word, char_mapping)
        ]

        score_improved = False

        #This is only place where I could use you multi proccesing , but we have already optimized the code pretty well
        for idx, match in matches[:20]:
            # Append to the pq the (char_mapping, cypher_index)
            # with priority (score, idx in dictionary freq)
            # Populate char_mapping
            word_mapping = dict(zip(cypher_word, match))
            # Check if new mapping does not conflict with what we
            # currently have
            word_mapping = {
                k: v for k, v in word_mapping.items() if k not in char_mapping
            }
            if set(word_mapping.values()) & set(char_mapping.values()):
                continue
            word_mapping.update(char_mapping)
            score = get_score(cypher_words, word_mapping, words)
            if score >= current_score:
                score_improved = True
            add_to_queue(word_mapping, cypher_index+1, priority=-score)


        if not matches or not score_improved:
            # Requeue for the next cypher_word
            # current_score = get_score(cypher_words, char_mapping, words)
            add_to_queue(char_mapping, cypher_index+1, priority=-current_score)

    return char_mapping


if __name__ == '__main__':
    with open("cipher.txt",encoding="utf8") as f:
        cypher_text = f.read()

    start = time.time()
    trans = decrypt(cypher_text)
    dt = time.time() - start
    decrypted_textfile = open("decrypted.txt","w") #Writing the decrypted text to the text file 
    decrypted_textfile.write(translate(cypher_text, trans, case_sensitive=True))
    decrypted_textfile.close()
    print("Please check two text files for output")
    print("Timing: {:.3f} sec".format(dt))

    new_dict = dict([(value, key) for key, value in trans.items()]) 
    key_textfile = open("key.txt","w") #Writing the decrypted key to the text file 
    for k,v in sorted(new_dict.items()):
        key_textfile.write(f"{k.upper()} = {v.upper()}" + "\n")
    key_textfile.close()

"Just for assurance, cipher.txt will be left in the same folder as this program and will have no text inside it.I will have all my test files in a separate folder which you can view to see how I tested this program"
"You can insert the cipher text into this file instead of changing line 228, if you wish to do so."
"Please check inputfilename-decrypted.txt and inputfilename-key.txt for the output of this program"
