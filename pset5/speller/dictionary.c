// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <strings.h>
#include <stdlib.h>
#include <string.h>

#include "dictionary.h"

// Represents number of buckets in a hash table
#define N 26

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Represents a hash table
node *hashtable[N];


// for size function later
int sizeDict = 0;
unsigned int sizeDictUn;

// Hashes word to a number between 0 and 25, inclusive, based on its first letter
unsigned int hash(const char *word)
{
    return tolower(word[0]) - 'a';
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Initialize hash table
    for (int i = 0; i < N; i++)
    {
        hashtable[i] = NULL;
    }

    // Open dictionary
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        unload();
        return false;
    }

    // Buffer for a word
    char word[LENGTH + 1];

    // Insert words into hash table
    while (fscanf(file, "%s", word) != EOF)
    {
        // increment sizeDict by 1 for each word read into dict
        sizeDict ++;

        // make new node that will be put into hash table; return false if run out of memeory
        node *new_node = malloc(sizeof(node));
        if (new_node == NULL)
        {
            unload();
            return false;
        }

        // sets value part of node to the word that is read in the dictionary
        strcpy(new_node->word, word);

        // use hash function to determine where word should go in the hash (what linked list should it be a part of)
        int x = hash(word);

        // insert new node into begining of linked list (head is the pointer to the start of the linked list)
        new_node->next = hashtable[x];
        hashtable[x] = new_node;
    }

    // Close dictionary
    fclose(file);

    // Indicate success
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    if (sizeDict > 0)
    {
        // cast sizeDict to unsigned int
        sizeDictUn = (unsigned int)sizeDict;
        return sizeDictUn;
    }
    return 0;
}

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // x = the index of the linked list to check; run hash funciton to get it
    int x = hash(word);

    // create new head as to not alter the link in the original hash table
    node *head = hashtable[x];

    // while head is not pointing to a NULL value
    while (head != NULL)
    {
        // if the value which head points to is the same as word, return true strcasecmp is case insensitive
        if (strcasecmp(head->word, word) == 0)
        {
            return true;
        }
        // set head to be the next pointer (head -> [word][next] -> [word2][next2]    ----  head now next therefore next -> [word2][next] ->... )
        head = head->next;
    }

    return false;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        // set header pointer pointing to the index of the hash table where we want to delete all nodes from - stop loop when reach NULL (no more nodes)
        node *head = hashtable[i];
        while (head != NULL)
        {
            // initialise temp pointer to the same thing head points to
            node *tmp = head;

            // move head pointer on as to not lose the rest of the linked list
            head = head->next;

            // finally, free whatever head was originally pointing to
            free(tmp);
        }
        // if the loop runs all the way until i = 25, then all nodes from each index in the hashtable are deleted; SUCCESS!
        if (i == 25)
        {
            return true;
        }
    }
    return false;
}