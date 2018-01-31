#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <string.h>

void caeserit(int user_key, string user_input);

int main(int argc, string argv[])
{

    if (argc != 2 || atoi(argv[1]) <= 0)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    } else {
        int user_key = 0;
        user_key = atoi(argv[1]);
        string user_text = GetString();
        caeserit(user_key, user_text);
    }

}

void caeserit(int user_key, string user_input)
{
    int result;
    
    char buffer [strlen(user_input)];

    for(int i = 0, j = strlen(user_input); i < j; i++)
    {
        if(isalpha(user_input[i]))
        {

                if(islower(user_input[i]))
                {

                    result = (user_input[i]-97);
                    result = (result+user_key)%26;
                    result += 97;
                    // sprintf(buffer, "%c", result);
                    buffer[i] = (char)result;
                    
                }
    
                if(isupper(user_input[i]))
                {
                    result = (user_input[i]-65);
                    result = (result+user_key)%26;
                    result += 65;
                    // sprintf(buffer, "%c", result);
                    buffer[i] = (char)result;

                }
        } else {
            // sprintf(buffer, "%c", user_input[i]);
            buffer[i] = (char)user_input[i];

        }
        
    }
    printf("%s\n", buffer);
}