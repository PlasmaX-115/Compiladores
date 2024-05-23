import re

FILE_NAME = 'entrada.txt'


def main():
    with open(FILE_NAME) as archivo:
        info = archivo.read()
    for word in re.findall(r"[A-Za-z']+", info):
        print(word.lower())

if __name__ == '__main__':
    main()
