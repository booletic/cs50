#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <string.h>

int main(void)
{
    string user_input = 0;
    user_input = GetString();
    int len_of_user_input = strlen(user_input);
    
    if(!isspace(user_input[0]))
    {
        printf("%c",toupper(user_input[0]));
    }
    
    for(int x = 0; x < len_of_user_input; x++)
    {
        if(isspace(user_input[x]))
        {
            printf("%c", toupper(user_input[x+1]));
        }
    }
    printf("\n");
}