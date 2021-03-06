import argparse

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

def ireplace(old, new, rule, text, ignore):
    idx = 0
    while idx < len(text):
        if ignore:
            index_l = text.lower().find(rule.lower(), idx)
            index_w = text.lower().find(old, index_l)
        else:
            index_l = text.find(rule, idx)
            index_w = text.find(old, index_l)
        if index_l == -1:
            return text

        text = text[:index_w] + new + text[index_w + len(old):]
        idx = index_w + len(old)
    return text

for d in dlist:
    with open('dicts/' + d, 'r') as dic:
        allVocs = dic.readlines()
    print('Started ' + d + '. ' + str(len(allVocs)) + ' entries')
    count = 1
    title = allVocs[0]

    for line in allVocs[1:]:
        if count % 4000 == 0:
            print(count)
        if line.find('||') == 0:
            word = title[0:title.find('=')]
            newWord = line[line.find('=') + 1:].strip()
            if line[2] == '$':
                rule = line[3:line.find('=')]
                ignore = False
            else:
                rule = line[2:line.find('=')]
                ignore = True
            text = ireplace(word, newWord, rule, text, ignore)
        else:
            title = line

        count += 1

    print('Finished ' + d)
 
with open(args.o, 'w') as out:
    out.write(text)