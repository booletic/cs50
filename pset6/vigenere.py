import cs50
import sys


def main():

    if len(sys.argv) == 2 and sys.argv[1].isalpha():
        print("plaintext: ", end="")
        pln_txt = cs50.get_string()
        alpha_ky = sys.argv[1]
        alpha_ky_list = list(alpha_ky)
        ky = list()
        cphr_txt = ""
        i = 0

        for k in alpha_ky_list:
            if k.isupper():
                ky.append(str(ord(k) - 65))
            elif k.islower():
                ky.append(str(ord(k) - 97))

        for pln_lttr in pln_txt:
            i %= len(alpha_ky)
            if pln_lttr.isalpha():
                if pln_lttr.isupper():
                    if (ord(pln_lttr) + int(ky[i])) > 90:
                        cphr_txt += chr((ord(pln_lttr) + int(ky[i])) - 26)
                    else:
                        cphr_txt += chr(ord(pln_lttr) + int(ky[i]))

                elif pln_lttr.islower():
                    if (ord(pln_lttr) + int(ky[i])) > 122:
                            cphr_txt += chr((ord(pln_lttr) + int(ky[i])) - 26)
                    else:
                            cphr_txt += chr(ord(pln_lttr) + int(ky[i]))

                i += 1

            else:
                cphr_txt += pln_lttr

        print("ciphertext: {}".format(cphr_txt))
    else:
        print("Usage: ./vigenere keyword")
        exit(1)


if __name__ == "__main__":
    main()