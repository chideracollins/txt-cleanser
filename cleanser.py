import os
import re
from dotenv import load_dotenv

load_dotenv()
files = [os.getenv("FILE_1"), os.getenv("FILE_2"), os.getenv("FILE_3")]
save_path = os.getenv("SAVE_PATH")
SENTENCE = ""


def clean_data(words_list, save_file):
    global SENTENCE
    bad_pattern = re.compile("[0-9()\/:;.,-]|.+[A-HJ-Z]|^[\u2019a-zA-Z]+$")
    end_pattern = re.compile(r"(!|\.|\?)$")
    comma_pattern = re.compile(",$")
    for word in words_list:
        if comma_pattern.search(word):
            word = word.replace(",", "")
        elif end_pattern.search(word):
            word = end_pattern.sub("\n", word)
            SENTENCE += word
            if bad_pattern.search(SENTENCE):
                SENTENCE = ""
                continue
            write_func(save_file, SENTENCE)
            SENTENCE = ""
            continue
        word += " "
        SENTENCE += word


def write_func(write_file, sentence):
    write_file.write(sentence)


def extract_func(save_file, file):
    global SENTENCE
    pattern = re.compile("[\u2019a-zA-Z0-9!:;,.\?()''/\"-]+")
    with open(file, "rt", encoding="utf-8") as read_file:
        for line in read_file:
            reading = pattern.findall(line)
            clean_data(reading, save_file)
    SENTENCE = ""


def main(files, save_path):
    with open(save_path, "at", encoding="utf-8") as save_file:
        for file in files:
            extract_func(save_file, file)
    print("Done Writing!")


main(files, save_path)
