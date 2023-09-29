// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <strings.h>

#include "dictionary.h"

// TODO: Choose number of buckets in hash table
const unsigned int N = 26;

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Hash table
node *table[N][N];

//A count of loaded words
int count = 0;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // Create a new temporary node
    node *compare;

    //Chech length of word
    int length = strlen(word);
    if (length == 1)
    {
        //Assign the temporary node value of first node
        compare = table[hash(word)][hash(word)];

        //Search same word at dictionary
        while (compare != NULL)
        {
            if (strcasecmp(word, compare->word) == 0)
            {
                return true;
            }
            //Assign the temporary node value of next node
            compare = compare->next;
        }
    }
    else
    {
        //Assign the temporary node value of first node
        compare = table[hash(word)][hash(&word[1])];

        //Search same word at dictionary
        while (compare != NULL)
        {
            if (strcasecmp(word, compare->word) == 0)
            {
                return true;
            }
            //Assign the temporary node value of next node
            compare = compare->next;
        }
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    //Check letters
    if (isalpha(word[0]) == 0)
    {
        return 25;
    }

    return toupper(word[0]) - 'A';
}


// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    //Open dictionary
    FILE *dictionary_words = fopen(dictionary, "r");
    if (dictionary_words == NULL)
    {
        printf("Can't open the file\n");
        fclose(dictionary_words);
        return 1;
    }
    // Create a buffer
    char buffer[LENGTH + 1];

    // Copy words
    while (fscanf(dictionary_words, "%s", buffer) != EOF)
    {
        //Increase count of dictionary's words
        count++;

        //Create a new node in the memory
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            printf("Not enough memory for n\n");
            free(n);
            fclose(dictionary_words);
            return 2;
        }

        // Create a node for a new word
        strcpy(n->word, buffer);
        n->next = NULL;

        //Check word's length
        int length = strlen(n->word);
        if (length == 1)
        {
            //Assign the hash function a value of word
            if (table[hash(n->word)][hash(n->word)] == NULL)
            {
                table[hash(n->word)][hash(n->word)] = n;
            }
            else
            {
                //Create a new node for change the pointer
                node *k = n;
                n->next = table[hash(n->word)][hash(n->word)];
                table[hash(n->word)][hash(n->word)] = k;
            }
        }
        else
        {
            //Assign the hash function a value of word
            if (table[hash(n->word)][hash(&n->word[1])] == NULL)
            {
                table[hash(n->word)][hash(&n->word[1])] = n;
            }
            else
            {
                //Create a new node for change the pointer
                node *k = n;
                n->next = table[hash(n->word)][hash(&n->word[1])];
                table[hash(n->word)][hash(&n->word[1])] = k;
            }
        }
    }

    //Close the file
    fclose(dictionary_words);

    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    //Count of dictionary's words
    return count;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    //Free all the nodes
    for (int i = 0; i < N; i++)
    {
        for (int k = 0; k < N; k++)
        {
            //Create a new node
            node *compare = table[i][k];
            while (compare != NULL)
            {
                //Create a new node
                node *tmp = compare;
                //Assign node a next value
                compare = compare->next;
                //Free first node
                free(tmp);
            }
        }
    }
    return true;
}
