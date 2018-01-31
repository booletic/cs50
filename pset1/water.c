#include <stdio.h>
#include <cs50.h>

int main(void)
{
    int user_input = 0;
    int co_factor = 12; // 1-minute shower is akin to using 192 ÷ 16 = 12 bottles of water
    
    printf("minutes: ");
    user_input = GetInt();
    printf("bottles: %i\n", user_input*co_factor);
}