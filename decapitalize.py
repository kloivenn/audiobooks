import argparse
import re

parser = argparse.ArgumentParser(description='Whatever...')
parser.add_argument('-i', metavar='DIC-FILE', type=str,
                    help='input dic file')
parser.add_argument('-o', metavar='TXT-FILE', type=str,
                    help='input txt file')

args = parser.parse_args()

with open(args.o, 'w') as out:
    with open(args.i, 'r') as dic:
        line = dic.readline()
        while line:
            word = line[1:line.find("=")]
            wordCap = word[0].capitalize() + word[1:]
            out.write('\\b' + wordCap + '\\b' + '/s/' + word + '/s/r/s/1\n')
            line = dic.readline()
