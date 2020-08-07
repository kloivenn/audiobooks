import argparse
import re

parser = argparse.ArgumentParser(description='Whatever...')
parser.add_argument('-i', metavar='DIC-FILE', type=str,
                    help='input dic file')
parser.add_argument('-o', metavar='TXT-FILE', type=str,
                    help='input txt file')

args = parser.parse_args()
check = False
with open(args.o, 'w') as out:
    with open(args.i, 'r') as dic:
        line = dic.readline()
        while line:
            if line == '||':
                break
            if line[0:2] == '||':
                word = line[2:line.find("=")]
                wordCap = word[0].capitalize() + word[1:]
                check = True
            else:
                if check:
                    out.write('\\b' + wordCap + '\\b' + '/s/' + word + '/s/r/s/1\n')
                check = False
            line = dic.readline()
