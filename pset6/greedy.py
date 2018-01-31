import cs50

while True:
    print("How much change owend? ", end="")
    user_input = cs50.get_float()
    if user_input > 0:
        break

user_input_int = round(user_input * 100)

quarters_counter = user_input_int // 25
user_input_int = user_input_int % 25

dimes_counter = user_input_int // 10
user_input_int = user_input_int % 10

nickels_counter = user_input_int // 5
user_input_int = user_input_int % 5

pennies_counter = user_input_int

print("{}".format(quarters_counter
                  + dimes_counter
                  + nickels_counter
                  + pennies_counter))