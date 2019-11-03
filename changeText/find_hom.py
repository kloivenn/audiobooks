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

with open(args.o, 'w') as out:
    for d in dlist:
        with open('dicts/' + d, 'r') as dic:
            allVocs = dic.readlines()
        print('Started ' + d + '. ' + str(len(allVocs)) + ' entries')
        count = len(allVocs) - 1
        prevTitle = count + 1

        while count >= 0:
            if count % 4000 == 0:
                print(count)
            line = allVocs[count]    

            if not line.find('||') == 0:
                word = '\\b' + line[0:line.find('=')] + '\\b'
                for m in re.finditer(word, text, flags = re.IGNORECASE):
                    textPiece = text[max(0, m.start() - 40):min(len(text) - 1, m.start() + 45)].replace('\n', ' ')
                    out.write(line)
                    out.write(str(count + 1) + "\n")
                    out.write(textPiece + "\n")
                    for i in range(count + 1, prevTitle):
                        if allVocs[i][2] == '$':
                            rule = allVocs[i][3:allVocs[i].find('=')]
                            if not textPiece.find(rule) == -1:
                                out.write(allVocs[i])
                        else:
                            rule = allVocs[i][2:allVocs[i].find('=')]
                            if not textPiece.lower().find(rule.lower()) == -1:
                                out.write(allVocs[i])
                    out.write("-----------\n")
                prevTitle = count
            count -= 1

        print('Finished ' + d)
 
