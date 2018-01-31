#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <string.h>
    
int main(int argc, string argv[])
{

    if(argc != 2 || isalpha(argv[1][0]) == 0)
    {
        printf("Usage: ./caesar keyword\n");
        return 1;
    }
    else
    {
        
        int key_len = strlen(argv[1]);
        
        for(int i = 0; i < key_len; i++)
        {
            if(isalpha(argv[1][i]) == 0)
            {
                printf("Usage: only keyword with alpha are valid\n");
                return 1;
                // break;
            }
        }
        
        char key_buffer[key_len];

        for(int i = 0; i < key_len; i++)
        {
            if(islower(argv[1][i]) != 0)
            {
                key_buffer[i] = (int)argv[1][i]-97;
            } else if(isupper(argv[1][i]) != 0)
            {
                key_buffer[i] = (int)argv[1][i]-65;
            }
        }
        
        string user_text = GetString();
        int string_len = strlen(user_text);
        int key_index = 0;
        char output_buffer[string_len];

        for(int i = 0; i < string_len; i++)
        {
            key_index %= key_len;
            
            if (isalpha(user_text[i]))
            {
                if(islower(user_text[i]))
                {
                    output_buffer[i] = (((user_text[i]-97)+key_buffer[key_index])%26)+97;
                }
                
                if(isupper(user_text[i]))
                {
                    output_buffer[i] = (((user_text[i]-65)+key_buffer[key_index])%26)+65;
                }
                
                key_index++;
            }
            else
            {
                output_buffer[i] = user_text[i];
            }

        }
        
        for(int i = 0; i < string_len; i++)
        {
            printf("%c", output_buffer[i]);
        }

        printf("\n");
    }

    
}