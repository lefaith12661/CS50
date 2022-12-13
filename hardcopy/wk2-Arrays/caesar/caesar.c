#include <cs50.h> //string and bool
#include <stdio.h> // printf
#include <string.h> // strlen
#include <ctype.h> // isdigit
#include <stdlib.h> // atoi

bool only_digits(string s);
char rotate(char c, int n);

int main(int argc, string argv[])
{
    // declare the key
    string key = argv[1];

    // Ensure single command-line argument
    // calls only_digits function on argv[1]
    if (argc != 2 || !only_digits(key))
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    // convert string argv[1] to int
    int k = atoi(key);

    // prompt user for plaintext
    string plaintext = get_string("plaintext:  ");

    // print string ciphertext
    printf("ciphertext: ");


    // for each character in the plaintext
    for (int i = 0, n = strlen(plaintext); i < n; i++)
    {
        // if it's a letter, rotate the character
        if (isalpha(plaintext[i]))
        {
            printf("%c", (rotate(plaintext[i], k)));
        }
        // else, unchanged
        else
        {
            printf("%c", plaintext[i]);
        }
    }
    printf("\n");
}

// Input: s (string)
// Output: true or false (bool)
bool only_digits(string s)
{
    for (int i = 0, n = strlen(s); i < n; i++)
    {
        if (!isdigit(s[i]))
        {
            return false;
        }
    }
    return true;
}

// Input: char c, int n
// Output: cipher (char)
char rotate(char c, int n)
{
    char cipher;
    if (isupper(c))
    {
        cipher = ((c - 'A') + n) % 26 + 'A';
    }
    else if (islower(c))
    {
        cipher = ((c - 'a') + n) % 26 + 'a';
    }
    else
    {
        cipher = c;
    }
    return cipher;
}