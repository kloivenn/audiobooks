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
        count = 1
        line = dic.readline()
        while line:
            #print(count)
            r = line.replace('\n', '').split('/s/')
            if r[2] == 'b':
                r[0] = '\\b' + r[0] + '\\b'
            if r[2] == 'r':
                r[0] = r[0] + '\\b'
            if r[2] == 'l':
                r[0] = '\\b' + r[0]
            if int(r[3]) == 0:
                fl = re.IGNORECASE
            else:
                fl = 0
            text = re.sub(r[0], r[1], text, flags = fl)
            line = dic.readline()
            count += 1
    print('Finished ' + d)

with open(args.o, 'w') as out:
    out.write(text)