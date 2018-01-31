import cs50

flag = True
while flag:
    print("height: ", end="")
    steps = cs50.get_int()
    if steps > 0 and steps < 24:
        for step in range(steps):
            print(" " * (steps-(step+1)), end="")
            print("#" + "#" * (step+1))
            flag = False