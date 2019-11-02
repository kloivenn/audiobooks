import argparse
import re
import fileinput

parser = argparse.ArgumentParser(description='Some description')
parser.add_argument('-i', metavar='TXT-FILE', type=str,
                    help='input file')
parser.add_argument('-o', metavar='TXT-FILE', type=str,
                    help='output file')
parser.add_argument('-d', metavar='TXT-FILE', type=str,
                    help='dictionary')
parser.add_argument('-dl', metavar='TXT-FILE', type=str,
                    help='dictionary list')
parser.add_argument('-c', type=bool, help='whether to count matches', default=False)

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
    matches = [];
    count = 1

    for line in allVocs:
        if count % 4000 == 0:
            print(count)
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
        if args.c:
            if re.search(r[0], text, flags = fl):
                matches.append(count)
        text = re.sub(r[0], r[1], text, flags = fl)
        count += 1

    print('Finished ' + d)
    if args.c:
        for i in matches:
            r = allVocs[i].replace('\n', '').split('/s/')
            if len(r) == 4:
                r.append(str(1))
            else:
                r[4] = str(int(r[4]) + 1)
            allVocs[i] = '/s/'.join(list(map(str, r))) + '\n'
        with open('dicts/' + d, 'w') as out:
            out.write(''.join(allVocs))
 
with open(args.o, 'w') as out:
    out.write(text)