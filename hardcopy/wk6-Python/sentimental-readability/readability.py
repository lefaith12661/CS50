# importing library
from cs50 import get_string


def main():
    # prompting user for text
    text = get_string("Text: ")

    # calculating parameters
    letter = count_letters(text)
    word = count_words(text)
    sentence = count_sentences(text)

    # L is the average number of letters per 100 words in the text
    L = letter / (word / 100.00)

    # S is the average number of sentences per 100 words in the text
    S = sentence / (word / 100.00)

    grade = round(0.0588 * L - 0.296 * S - 15.8)

    # print out grade level
    if grade >= 16:
        print(f"Grade 16+")
    elif grade < 1:
        print(f"Before Grade 1")
    else:
        print(f"Grade {grade}")


# Input: text (string)
# Output: num letters (int)
def count_letters(text):
    nletter = 0
    for i in range(len(text)):
        if str.isalpha(text[i]):
            nletter += 1
    return nletter


# Input: text (string)
# Output: num words (int)
def count_words(text):
    nword = 1
    for i in range(len(text)):
        if str.isspace(text[i]):
            nword += 1
    return nword


# Input: text (string)
# Output: num sentences (int)
def count_sentences(text):
    nsentence = 0
    for i in range(len(text)):
        if (text[i] == '.') or (text[i] == '!') or (text[i] == '?'):
            nsentence += 1
    return nsentence


main()