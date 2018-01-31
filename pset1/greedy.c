#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void)
{
    float user_input = 0.0;
    
    int user_input_int = 0;
    int quarters_value = 25, dimes_value = 10, nickels_value = 5;
    int quarters_counter = 0, dimes_counter = 0, nickels_counter = 0, pennies_counter = 0;
  
    do
    {
    printf("How much change owned? ");
    user_input = GetFloat()*100;
    } while(user_input <= 0);
    
    // printf("%f\n", user_input);
    user_input = (float)round(user_input);
    // printf("%f\n", user_input);
    user_input_int = (int)user_input;
    // printf("%i\n", user_input_int);

    
    while(user_input_int >= quarters_value)
    {
        quarters_counter++;
        user_input_int = user_input_int-quarters_value;
    }
    
    // printf(">>>%i\n", user_input_int);

    while(user_input_int >= dimes_value)
    {
        // printf(">>>%i\n", user_input_int);
        dimes_counter++;
        user_input_int = user_input_int-dimes_value;
    }
    
    while(user_input_int >= nickels_value)
    {
        nickels_counter++;
        user_input_int = user_input_int-nickels_value;
    }
    
    if(user_input_int >= 0)
    {
        pennies_counter = user_input_int;
    }
    
    // printf("%i quarters, %i dimes, %i nickels, %i pennies\n", quarters_counter, dimes_counter, nickels_counter, pennies_counter);
    // printf("%i quarters, %i pennies\n", quarters_counter, pennies_counter);
    printf("%i\n", quarters_counter+dimes_counter+nickels_counter+pennies_counter);
}