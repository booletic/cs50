import cs50
import sys


def main():

    if len(sys.argv) == 2 and sys.argv[1].isdecimal():
        print("plaintext: ", end="")
        plain_text = cs50.get_string()
        key = int(sys.argv[1]) % 26
        cipher_text = ""

        for plain_letter in plain_text:
            if plain_letter.isalpha() and plain_letter.isupper():
                if (ord(plain_letter) + key) > 90:
                    cipher_text += chr((ord(plain_letter) + key) - 26)
                else:
                    cipher_text += chr(ord(plain_letter) + key)

            elif plain_letter.isalpha() and plain_letter.islower():
                if (ord(plain_letter) + key) > 122:
                    cipher_text += chr((ord(plain_letter) + key) - 26)
                else:
                    cipher_text += chr(ord(plain_letter) + key)

            else:
                cipher_text += plain_letter

        print("ciphertext: {}".format(cipher_text))
    else:
        print("Usage: ./caesar k")
        exit(1)


if __name__ == "__main__":
    main()