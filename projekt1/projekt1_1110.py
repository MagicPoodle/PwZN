import argparse
from ascii_graph import Pyasciigraph
from ascii_graph.colors import *
from ascii_graph.colordata import vcolor
import re


def sorter(a):
    return a[1]


big_words_list = []
his_words_list = []

parser = argparse.ArgumentParser(description="Opis")
parser.add_argument('-file', help='name of file', default='nic-dwa-razy.txt')
parser.add_argument('-w', '--words', help="number of words in histogram", type=int, default='10')
parser.add_argument('-n', '--number', help='minimal number of letter in words ', type=int, default='0')
args = parser.parse_args()

file = open(args.file, "r", encoding='utf8')
word_list = re.sub(r'[,.()/!-?]', "", file.read()).strip().split()
unique_word_list = list(set(word_list))

for word in unique_word_list:
    counter = 0
    for duplicate_word in word_list:
        if duplicate_word == word:
            counter = counter + 1
    big_words_list.append((word, counter))
big_words_list.sort(key=sorter, reverse=True)

for elements in big_words_list:
    if len(his_words_list) < args.words:
        if len(elements[0]) >= args.number:
            his_words_list.append(elements)

print(f'\nFile name : {args.file}')
print(f'Numer of words in histogram : {args.words}')
print(f'Minimal number of letter in words : {args.words} \n')

graph = Pyasciigraph()
pattern = [Gre, Yel, Red, Blu]
data = vcolor(his_words_list, pattern)
graph = graph.graph('Histogram', data)
for line in graph:
    print(line)