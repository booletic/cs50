/**
 * dictionary.c
 *
 * Computer Science 50
 * Problem Set 5
 *
 * Implements a dictionary's functionality.
 */
 
#include <stdbool.h>
#include "dictionary.h"
#include "stdio.h"
#include "stdlib.h"
#include <ctype.h>
#include <string.h>

// the size of the hashtable
#define HASHSIZE 250000

// a varaible to keep track of the words in the data structure
int dictSize = 0;

// creating nodes for linked list
typedef struct node
{
    char word[LENGTH+1];
    struct node* next;
} node;

// create the hash table
node * hashtable[HASHSIZE] = {NULL};

// a hash function from The C Programming Language 2nd ed. book
int hash(const char* word)
{
    unsigned hashVal = 0;
    for(hashVal = 0; *word != '\0'; word++)
    {
        hashVal *= 31;
        hashVal += *word;
    }
    return hashVal % HASHSIZE;
}

/**
 * Returns true if word is in dictionary else false.
 */
bool check(const char* word)
{
    // word to lower case
    int n = 0;
    n = strlen(word);
    char wordLower[n+1];
    for (int i = 0; i < n; i++)
         wordLower[i] = tolower(word[i]);
     wordLower[n] = '\0';
     
    
    // chech the word in text againt the dictionary
    int index = hash(wordLower);
    node* cmpNode =  (hashtable[index] != NULL) ? hashtable[index] : NULL;    
    for (;cmpNode != NULL;)
    {
        if (strcmp(wordLower, cmpNode->word) == 0)
            return true;
        cmpNode = cmpNode->next;
    }
    return false;
}

/**
 * Loads dictionary into memory.  Returns true if successful else false.
 */
bool load(const char* dictionary)
{
    // load the dictionary in read mode
    FILE* dictFile = fopen(dictionary, "r");
    if (dictFile == NULL)
        return false;

    // load dictionary words to the hashtable
    char word[LENGTH+1];
    for (;fscanf(dictFile, "%s\n", word) != EOF;)
    {
        node* dictWord = malloc(sizeof(node));
        strcpy(dictWord->word, word);
        int hashIndex = hash(word);
        
        dictWord->next = (hashtable[hashIndex] != NULL) ? hashtable[hashIndex] : NULL;
        hashtable[hashIndex] = dictWord;
        
        dictSize++;
    }
    fclose(dictFile);
    return true;
}

/**
 * Returns number of words in dictionary if loaded else 0 if not yet loaded.
 */
unsigned int size(void)
{
    // dictionary size, this is a global varaible that gets updated in the load function
    return dictSize;
}

/**
 * Unloads dictionary from memory.  Returns true if successful else false.
 */
bool unload(void)
{
    // free memory from data allocated by load
    int index = 0;

    for (;index < HASHSIZE;)
    {
        for (;hashtable[index] != NULL;)
        {
            node* temp = hashtable[index];
            hashtable[index] = temp->next;
            free(temp);
        }
        index++;
    }
    return true;
}