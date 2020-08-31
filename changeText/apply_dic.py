import argparse
import re

parser = argparse.ArgumentParser(description='Some description')
parser.add_argument('-i', metavar='TXT-FILE', type=str,
                    help='input file')
parser.add_argument('-o', metavar='TXT-FILE', type=str,
                    help='output file')
parser.add_argument('-d', metavar='TXT-FILE', type=str,
                    help='dictionary')
parser.add_argument('-dl', metavar='TXT-FILE', type=str,
                    help='dictionary list')

args = parser.parse_args()

if args.d:
    dlist = [args.d]
else:
    if args.dl is None:
        print('No dictionary or dictionary list')
        exit()
    with open(args.dl, 'r') as f:
        dlist = list(map(lambda el: el.replace('\n', ''), f.readlines()))

with open(args.i, 'r') as f:
    text = f.read()

for d in dlist:
    with open('dicts/' + d, 'r') as dic:
        allVocs = dic.readlines()
    print('Started ' + d + '. ' + str(len(allVocs)) + ' entries')
    count = 1

    for line in allVocs:
        if count % 4000 == 0:
            print(count)
        flag = re.IGNORECASE
        if line[0] == "$":
            flag = 0
            line = line[1:]
        word = '\\b' + line[0:line.find('=')] + '\\b'
        newWord = line[line.find('=') + 1:].strip().replace('\\', '\\\\')
        text = re.sub(word, newWord, text, flags = flag)

        count += 1

    print('Finished ' + d)
 
with open(args.o, 'w') as out:
    out.write(text)