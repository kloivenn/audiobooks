import argparse
import re

parser = argparse.ArgumentParser(description='Whatever...')
parser.add_argument('-i', metavar='BXD-FILE', type=str,
                    help='input bxd file')
parser.add_argument('-o', metavar='TXT-FILE', type=str,
                    help='input txt file')

args = parser.parse_args()

skip = 3
with open(args.o, 'w') as out:
    with open(args.i, 'r') as dic:
        line = dic.readline()
        while line:
            if skip == 2:
                m = re.match('Delimiter=(.)', line)
                dmt = m.group(1)
            if skip <= 0:
                voc = line.replace('\n', '').split(dmt)
                if int(voc[4]) == 1:
                    voc[8] = re.sub(r'\$(\d+)', r'\\g<\1>', voc[8])
                else:
                	voc[7] = re.sub(r'(\)|\(|\.|\?|\+)', r'\\\1', voc[7])
                	voc[8] = re.sub(r'\(', r'\(', voc[8])
                	voc[8] = re.sub(r'\)', r'\)', voc[8])

                newLine = voc[7] + '/s/' + voc[8] + '/s/'
                voc[5] = int(voc[5])
                if voc[5] == 0:
                    if (not re.match(r'\w', voc[7][0])) & (int(voc[6]) == 0):
                        voc[5] += 2
                    if (not re.match(r'\w', voc[7][-1])) & (int(voc[6]) == 0):
                        voc[5] += 1
                    if voc[5] == 0:
                        newLine += 'b/s/'
                if voc[5] == 1:
                    if (not re.match(r'\w', voc[7][0])) & (int(voc[6]) == 0):
                        voc[5] += 2
                    else:
                        newLine += 'l/s/'
                if voc[5] == 2:
                    if (not re.match(r'\w', voc[7][-1])) & (int(voc[6]) == 0):
                        voc[5] += 1
                    else:
                        newLine += 'r/s/'
                if voc[5] == 3:
                    newLine += 'n/s/'
                newLine += voc[3] + '\n'
                out.write(newLine)
                if int(voc[6] == 1):
                    print(skip)
            skip -= 1
            line = dic.readline()
dic.close()
out.close()

print('Done. ' + str(-skip + 1) + ' lines parsed.')