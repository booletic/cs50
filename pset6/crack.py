import crypt
import itertools
import sys


def main():
    if (len(sys.argv) == 2 and
       sys.getsizeof(sys.argv[1]) == 62 and sys.argv[1][:2].isalnum()):
        userinput = sys.argv[1]
    else:
        print("Usage: ./crack hash")
        exit(1)

    lcase = "abcdefghijklmnopqrstuvwxyz"
    ucase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    wordlist = list()

    for i in range(4):
        wordlist += list(itertools.product(lcase + ucase, repeat=i + 1))
    for i in wordlist:
        password = "".join(i)
        if crypt.crypt(password, userinput[:2]) == userinput:
            print(password)
            break


if __name__ == "__main__":
    main()