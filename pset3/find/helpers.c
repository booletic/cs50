/**
 * helpers.c
 *
 * Computer Science 50
 * Problem Set 3
 *
 * Helper functions for Problem Set 3.
 */
       
#include <cs50.h>

#include "helpers.h"

/**
 * Returns true if value is in array of n values, else false.
 */
bool search(int value, int values[], int n)
{
    // TODO: implement a searching algorithm
    // if(value <= 0)
    // {
    //     return false;
    // }
    // for(int i =0; i < n; i++)
    // {
    //     if(value == values[i])
    //     {
    //         return true;
    //     }
    // }
    // return false;
    
    int right = n;
    int left = 0;
    int middle;
    
    while(right >= left)
    {
        middle = (right+left)/2;
        
        if(value == values[middle])
        {
            return true;
        }
        else if(value < values[middle])
        {
            right -= middle;
        }
        else
        {
            left += middle;
        }
    }
    
    return false;
}

/**
 * Sorts array of n values.
 */
void sort(int values[], int n)
{
    // TODO: implement an O(n^2) sorting algorithm
    // return;
    int min, temp;
    
    for(int i = 0; i < n-1; i++)
    {
        min = i;
        
        for(int j = i+1; j < n; j++)
        {
            if(values[j] < values[min])
            {
                min = j;
            }
        }
        
        if(min != i)
        {
            temp = values[i];
            values[i] = values[min];
            values[min] = temp;
        }
    }
}