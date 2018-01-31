import cs50


def chck_sum(crd_nm):
    ttl = 0
    crd_nm = str(crd_nm)[::-1]

    for i in range(len(str(crd_nm))):
        if i & 1:
            dgt = int(str(crd_nm)[i]) * 2
        else:
            dgt = int(str(crd_nm)[i])

        if dgt > 9:
            dgt = dgt - 9
        ttl = ttl + dgt

    return ((ttl % 10) == 0)


def main():
    AMEX = "34", "37"
    MASTERCARD = "51", "52", "53", "54", "55",
    VISA = "4"

    print("Number: ", end="")
    crd_nm = cs50.get_int()
    crd_str = str(crd_nm)

    if (crd_str.startswith(AMEX)
            and len(crd_str) == 15 and chck_sum(crd_nm)):
        print("AMEX")

    elif (crd_str.startswith(MASTERCARD)
          and len(crd_str) == 16 and chck_sum(crd_nm)):
        print("MASTERCARD")

    elif (crd_str.startswith(VISA)
          and len(crd_str) in {13, 16} and chck_sum(crd_nm)):
        print("VISA")

    else:
        print("INVALID")


if __name__ == "__main__":
    main()