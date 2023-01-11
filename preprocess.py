import os
import json

fr = {
    'A' : 8.496,
    'B'	: 2.072,
    'C'	: 4.538,
    'D'	: 3.384,
    'E'	: 11.160,
    'F'	: 1.812,
    'G'	: 2.470,
    'H'	: 3.003,
    'I'	: 7.544,
    'J'	: 0.196,
    'K'	: 1.101,
    'L'	: 5.489,
    'M'	: 3.012,
    'N'	: 6.654,
    'O'	: 7.163,
    'P'	: 3.167,
    'Q'	: 0.196,
    'R'	: 7.580,
    'S'	: 5.735,
    'T'	: 6.950,
    'U'	: 3.630,
    'V'	: 1.007,
    'W'	: 1.289,
    'X'	: 0.290,
    'Y'	:1.777,
    'Z'	: 0.272,
}


def vectorize(name):
    nname = []
    for i in name :
        nname.append(fr[upper(i)])
    return nname


def main():
    path = os.getcwd()
    path+="\\tutorial\\scientists"
    for sc in os.listdir(path):
        f = open(path + "\\"+sc,"r+")
        scient = json.load(f)
        print(str(scient))

if __name__ == "__main__" :
    main()
