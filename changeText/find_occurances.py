import argparse
import re

parser = argparse.ArgumentParser(description='Some description')
parser.add_argument('-t', metavar='TXT-FILE', type=str,
                    help='text')
parser.add_argument('-o', metavar='TXT-FILE', type=str,
                    help='output file')
parser.add_argument('-ph', metavar='TXT-FILE', type=str,
                    help='query phrase')

args = parser.parse_args()

with open(args.t, 'r') as f:
    text = f.read().replace('\xa0', ' ')
text_unsigned = text.replace('!', '.').replace('?', '.').replace('…', '.').replace('–', '-').replace('—', '-').replace('. -', ', -').replace('ё', 'е').replace('Ё', 'Е')


def getRegions(pos):
    before = text_unsigned[max((pos - 301), text_unsigned.rfind('\n', 0, pos - 1) - 1):pos]
    after = text_unsigned[(pos - 1):min((pos + 301), text_unsigned.find('\n', pos + 1))]
    dotFirst = max(before.rfind('.'), 0)
    dotLast = after.find('.')
    if dotLast == -1:
        dotLast = len(after)

    while len(before) - dotFirst + dotLast < 40:
        dotFirstNext = before.rfind('.', 0, dotFirst)
        dotLastNext = after.find('.', dotLast + 1)
        if dotLastNext == -1 and dotFirstNext == -1:
            break
        if dotLastNext == -1:
            dotFirst = dotFirstNext
        elif dotFirstNext == -1:
            dotLast = dotLastNext
        elif dotLastNext - dotLast > dotFirst - dotFirstNext:
            dotFirst = dotFirstNext
        else:
            dotLast = dotLastNext
            
    return before[dotFirst + 2:] + after[1:(dotLast + 1)]

out = open(args.o, "w")

with open(args.ph) as ph:
  for line in ph:
    line = line.rstrip()
    out.write("--- " + line + "\n")
    words = len(line.split(" "))
    found = False

    while not found and words > 0:
      occur = re.finditer("\\b" + line + "\\b", text, flags = re.IGNORECASE)
      for o in occur:
        found = True
        out.write(getRegions(round((o.start() + o.end())/2)) + "\n")
      if not found:
        if words % 2 == 0:
          line = line[(line.find(" ") + 1):]
        else:
          line = line[:line.rfind(" ")]
      words -= 1

out.close()