import csv
import re
import unidecode


def makePreprocess(filepath):
    with open(filepath, newline="", encoding="UTF-8") as input_file:
        lettore = csv.reader(input_file, delimiter=",")
        next(lettore)
        with open("Backend/FullDataset.csv", "a", newline="", encoding="UTF-8") as output_file:
            writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            i = 0
            for linea in lettore:

                linea[1:3] = [' '.join(linea[1:3])]

                for url in __FindURLs(linea[3]):
                    linea[3] = linea[3].replace(url, '')

                for char in __FindSpecialChar(linea[3]):
                    linea[3] = linea[3].replace(char, '')

                for mention in __FindMentions(linea[3]):
                    linea[3] = linea[3].replace(mention, '')

                linea[3] = linea[3].lower()

                linea[3] = unidecode.unidecode(linea[3])

                for mark in __FindMark(linea[3]):
                    linea[3] = linea[3].replace(mark, ' ')

                for space in __FindSpaces(linea[3]):
                    linea[3] = linea[3].replace(space, ' ')

                writer.writerow(linea)
                i = i + 1
        print(f"added {i} tweets")

def __FindURLs(string):
    url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string)
    pics = re.findall('pic.twitter.com/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',string)
    return url + pics


def __FindSpecialChar(string):
    char = re.findall('[#]', string)
    return char


def __FindMentions(string):
    char = re.findall('@[A-Za-z0-9_]+', string)
    return char


def __FindSpaces(string):
    char = re.findall(' +', string)
    return char


def __FindMark(string):
    char = re.findall(r'[^\w\s]', string)
    return char
