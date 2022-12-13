// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <strings.h> //strcasecmp
#include <string.h> //strlen
#include <stdio.h>
#include <stdlib.h>
#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Choose number of buckets in hash table
// N = 676: for all the combinations of the first two letters
const unsigned int N = (LENGTH * 'Z');

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // Hash word to obtain a hash value
    int hash_value = hash(word);

    // Access linked list at that hash value in the hash table
    node *cursor = table[hash_value];

    // Traverse linked list, looking for the word (strcasecmp)
    while (cursor != NULL)
    {
        if (strcasecmp(word, cursor -> word) == 0)
        {
            return true;
        }
        cursor = cursor -> next;
    }
    return false;
}

// Hashes word to a number, output hash code or location
// (const char *word) = string
unsigned int hash(const char *word)
{
    int sum_word = 0;
    for (int i = 0, n = strlen(word); i < n; i++)
    {
        sum_word += toupper(word[i]);
    }
    return (sum_word % N);
}

// Declaring variable
unsigned int word_count;
unsigned int hash_key;

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // open dictionary file
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        printf("Cannot open file\n");
        return false;
    }

    // declare word
    char word[LENGTH + 1];

    // read strings from file until fscanf returns EOF
    while (fscanf(file, "%s", word) != EOF)
    {
        // create a new node that stores the word inside hash table
        node *new_node = malloc(sizeof(node));
        if (new_node == NULL)
        {
            return false;
        }

        // copy word into that node
        strcpy(new_node -> word, word);

        /* call upon the hash function to determine which index/linked list
        into hash table when inserting this new node */
        hash_key = hash(word);

        // insert new node into hash table(array of linked lists)
        /* add a new node to a linked list so that you can...
        index into the hash table to get the linked list you want to use to add word
        set pointers in the correct order! */
        new_node -> next = table[hash_key];
        table[hash_key] = new_node;

        // word count
        word_count++;

    }
    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // Return the number of words that are in dictionary (file)
    return word_count;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    /* Iterate through hash table, going over each individual linked list,
    calling free on all of the nodes inside of those linked lists */
    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i];
        node *tmp = cursor;
        if (cursor != NULL)
        {
            // move cursor to the next node
            cursor = cursor -> next;
            // free temp
            free(tmp);
        }
    }
    // return true if successful
    return true;
}
