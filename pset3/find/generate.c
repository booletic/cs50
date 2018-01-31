/**
 * generate.c
 *
 * Computer Science 50
 * Problem Set 3
 *
 * Generates pseudorandom numbers in [0,LIMIT), one per line.
 *
 * Usage: generate n [s]
 *
 * where n is number of pseudorandom numbers to print
 * and s is an optional seed
 */
 
#define _XOPEN_SOURCE

#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// constant
#define LIMIT 65536

int main(int argc, string argv[])
{
    // TODO: validation if appended arguments are less that on or greater than 2, then exit.
    if (argc != 2 && argc != 3)
    {
        printf("Usage: generate n [s]\n");
        return 1;
    }

    // TODO: convert the first appended argument to integer, this is used for the for loop at line 50;
    int n = atoi(argv[1]);

    // TODO: if the argument has a seed, then run the function with the user seed.
    //       if the argument has no seed, then run the function with the unix time as a seed.
    if (argc == 3)
    {
        srand48((long int) atoi(argv[2]));
    }
    else
    {
        // printf("%li\n", time(NULL));
        srand48((long int) time(NULL));
    }

    // TODO: print the generated value n times, by definition the drand48 returns a double precision floating point,
    //       thus the product of drand and the limit is the output, lastly the output is casted to int and printed.
    for (int i = 0; i < n; i++)
    {
        printf("%i\n", (int) (drand48() * LIMIT));

    }

    // success
    return 0;
}