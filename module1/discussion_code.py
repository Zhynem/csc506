#!/Users/zhynem/.pyenv/shims/python3

# Get a list of dictionary words in lowercase for uniformity
with open("/usr/share/dict/words", "r") as f:
    dictionary = [word.strip() for word in f.readlines()]


def is_anagram(word1: str, word2: str) -> bool:
    # Make sure both words match the lowercase standard
    word1 = word1.lower()
    word2 = word2.lower()
    # Make sure both words have the same number of letters
    if len(word1) != len(word2):
        return False
    # Make sure both words use the same set of letters
    if set(word1) != set(word2):
        return False
    # Make sure the letter counts for each word is the same
    word1_letter_count = {
        l: v
        for (l, v) in zip(set(word1), [word1.count(letter) for letter in set(word1)])
    }

    word2_letter_count = {
        l: v
        for (l, v) in zip(set(word2), [word2.count(letter) for letter in set(word2)])
    }
    if word1_letter_count != word2_letter_count:
        return False
    # Make sure both words are in the dictionary
    if (word1 not in dictionary) or (word2 not in dictionary):
        return False
    # If all conditions were met then the words are anagrams of each other
    return True


# Run some tests
print(f"tea, eat | Anagram? {is_anagram('tea', 'eat' )}")
print(f"listen, silent | Anagram? {is_anagram('listen', 'silent' )}")
print(f"binary, brainy | Anagram? {is_anagram('binary', 'brainy' )}")
print(f"apple, pealp | Anagram? {is_anagram('apple', 'pealp' )}")
print(f"race, care | Anagram? {is_anagram('race', 'care' )}")
print(f"stone, tones | Anagram? {is_anagram('stone', 'tones' )}")
print(f"night, thing | Anagram? {is_anagram('night', 'thing' )}")
print(f"python, typhon | Anagram? {is_anagram('python', 'typhon' )}")
print(f"save, vase | Anagram? {is_anagram('save', 'vase' )}")
print(f"angel, glean | Anagram? {is_anagram('angel', 'glean' )}")
print(f"world, wordl | Anagram? {is_anagram('world', 'wordl' )}")
