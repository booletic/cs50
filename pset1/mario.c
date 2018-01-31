#include <stdio.h>
#include <cs50.h>

void build_pyramid(int user_input)
{
    char draw_air[2] = " ";
    char draw_solid = '#';

    
    for(int row = user_input-1; row != 0; row--)
    {
         for(int col = 0; col != user_input; col++)
         {
            if(row-1 <= col) {
                printf("%c", draw_solid);
            } else {
                printf("%s", draw_air);
            }
        }
        printf("\n");
    }
}

int main(void)
{

    int user_input = 0;
    
    do
    {
        printf("height: ");
        user_input = GetInt()+1;
        
    } while(user_input <= 0 || user_input > 24);
    
    build_pyramid(user_input);
    
}