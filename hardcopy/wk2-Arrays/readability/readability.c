#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    // prompt user for text
    string text = get_string("Text: ");

    // calculating parameters
    int letter = count_letters(text);
    int word = count_words(text);
    int sentence = count_sentences(text);

    // L is the average number of letters per 100 words in the text
    float L = letter / (word / 100.00);

    // printf("testing value: %d vs %f vs %f\n", (word / 100), (((float) word ) / 100), ((float) (word / 100)));
    // S is the average number of sentences per 100 words in the text
    float S = sentence / (word / 100.00);

    int grade = round(0.0588 * L - 0.296 * S - 15.8);

    // print out grade level
    if (grade >= 16)
    {
        printf("Grade 16+\n");
    }
    else if (grade < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", grade);
    }
}

// Input: text (string)
// Output: num letters (int)
int count_letters(string text)
{
    // num of letters
    int nletter = 0;

    for (int i = 0; i < strlen(text); i++)
    {
        // if letter -> count (nletter++)
        if (isalpha(text[i]))
        {
            nletter++;
        }
        // else (not letter) -> nothing
    }
    return nletter;
}

// // Input: text (string)
// // Output: num words (int)
int count_words(string text)
{
    // num of words
    int nword = 1;

    for (int i = 0; i < strlen(text); i++)
    {
        // if space -> count (nword ++)
        // will not start or end with space
        if (isspace(text[i]))
        {
            nword++;
        }
    }
    return nword;
}

// Input: text (string)
// Output: num sentences (int)
int count_sentences(string text)
{
// num of sentences
    int nsentence = 0;

    for (int i = 0; i < strlen(text); i++)
    {
        // if the i is not . or ! or ? -> count (nsentence ++)
        if ((text[i] == '.') || (text[i] == '!') || (text[i] == '?'))
        {
            nsentence++;
        }
    }
    return nsentence;
}
