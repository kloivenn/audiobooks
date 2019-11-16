import argparse
import re

parser = argparse.ArgumentParser(description='Some description')
parser.add_argument('-i', metavar='TXT-FILE', type=str,
                    help='input file')
parser.add_argument('-o', metavar='TXT-FILE', type=str,
                    help='output file')
parser.add_argument('-d', metavar='TXT-FILE', type=str,
                    help='dictionary')

args = parser.parse_args()

with open(args.i, 'r') as f:
    text = f.read()

def sort_list(list1, list2): 
    zipped_pairs = zip(list2, list1) 
    z = [x for _, x in sorted(zipped_pairs)] 
    return z 

words = []
counts =[]
for m in re.finditer(r'\b[А-ЯЁ]\w+', text):
    if m.group(0) in words:
        counts[words.index(m.group(0))] += 1
    else:
        words.append(m.group(0))
        counts.append(1)

with open('dicts/' + args.d, 'r') as f:
    dic = f.read()

i = 0
while i < len(words):
    if re.search('\\$' + words[i] + '=', dic):
        words.pop(i)
        counts.pop(i)
    else:
        i += 1

wordsSorted = sort_list(words, counts)

with open(args.o, 'w') as out:
    for w in wordsSorted:
        out.write(w + ' ' + str(counts[words.index(w)]) + '\n')