import argparse
import multiprocessing
from joblib import Parallel, delayed
import re
import itertools
import datetime
import random

num_cores = multiprocessing.cpu_count()

parser = argparse.ArgumentParser(description='Some description')
parser.add_argument('-i', metavar='TXT-FILE', type=str,
                    help='input file')
parser.add_argument('-o', metavar='TXT-FILE', type=str,
                    help='output file')
parser.add_argument('-log', metavar='TXT-FILE', type=str,
                    help='log file')
parser.add_argument('-d', metavar='TXT-FILE', type=str,
                    help='dictionary')
parser.add_argument('-n', metavar='TXT-FILE', type=str,
                    help='leave 1 out of n')

args = parser.parse_args()

if args.log and not args.n:
    args.n = 1

if not args.n or not args.log:
    args.n = 0
n = int(args.n) or 0

with open('dicts/' + args.d, 'r') as f:
    dictEntr = list(f.readlines())
with open(args.i, 'r') as f:
    text = f.read().replace('\xa0', ' ')
text_unsigned = text.replace('!', '.').replace('?', '.').replace('…', '.').replace('–', '-').replace('—', '-').replace('. -', ', -').replace('ё', 'е').replace('Ё', 'Е')

def getRegions(start, end):
    before = text_unsigned[max((start - 301), text_unsigned.rfind('\n', 0, start - 1) + 1):(start - 1)]
    after = text_unsigned[end:min((end + 301), text_unsigned.find('\n', end + 1))]
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
            
    return [before[dotFirst:], after[1:dotLast]]
    
    
def findOccur(ind, line):
    pos = []
    if line[0:2] == '||':
        word = line[2:line.find("=")]
        if text.find(word) != -1:
            occur = re.finditer('\\b' + word + '\\b', text)
            pos = list(map(lambda o: [ind, o.start(), getRegions(o.start(), o.end()) ], occur))
    return pos

t0 = datetime.datetime.now()
if __name__ == "__main__":
    allOcs = Parallel(n_jobs = num_cores)(delayed(findOccur)(ind, line) for ind, line in enumerate(dictEntr[:-1]))
print("Homographs found")
print((datetime.datetime.now() - t0).total_seconds()/60)
allOcs = list(itertools.chain.from_iterable(allOcs))

manager = multiprocessing.Manager()
log_dict = manager.dict({})

def makeDecision(pr, n):
    opts = dictEntr[pr[0]][(dictEntr[pr[0]].find('=') + 1):-1].split(',')
    if n == 0:
        rand = -1
    else:
        rand = random.randint(1, n)
    if dictEntr[pr[0] + 1][0:2] == '||':
        if rand == 1:
            log_dict[len(log_dict)] = pr[2][0] + ' _' + opts[0] + '_ ' + pr[2][1] + '\n'
        pr.append(opts[0])
        return pr
    scores = [0] * len(opts)
    insts = [0] * len(opts)
    opt = -1
    test = 1
    st = ''
    while opt < len(opts):
        line = dictEntr[pr[0] + test]
        if line.find(':') == -1:
            if rand == 1 and opt > -1:
                st += str(scores[opt]) + ': ' + before_log + ' _' + opts[opt] + '_ ' + after_log + '\n'
            opt += 1
            before_log = pr[2][0]
            after_log = pr[2][1]
        else:
            insts[opt] += line.count('|')
            testType = line[:line.find(':')]
            coef = testType.count('+') * 0.5 + 1
            testType = testType.replace('+', '')
            testBody = line[(line.find(':') + 1):-1]
            
            if len(testBody) > 0:  
                if testType == "before":
                    for o in re.finditer(testBody, pr[2][0], re.I):
                        scores[opt] += coef * max((o.end() - o.start())/4, 1) * max((20 - len(pr[2][0]) + o.end()), 1)**2
                        if rand == 1:
                            before_log = before_log[:o.start()] + before_log[o.start():o.end()].upper() + before_log[o.end():]
                elif testType == "after":
                    for o in re.finditer(testBody, pr[2][1], re.I):
                        scores[opt] += coef * max((o.end() - o.start())/4, 1) * max(20 - o.start() + 1, 1)**2
                        if rand == 1:
                            after_log = after_log[:o.start()] + after_log[o.start():o.end()].upper() + after_log[o.end():]
        test += 1

    maxScore = max(scores)
    maxInd = [i for i, j in enumerate(scores) if j == maxScore]
    resInd = maxInd[0]
    for ind in maxInd[1:]:
        if insts[ind] > insts[resInd]:
            resInd = ind
    if rand == 1:
        log_dict[len(log_dict)] = st + opts[resInd] + '\n'            
    pr.append(opts[resInd])
    return pr

t0 = datetime.datetime.now()
if __name__ == "__main__":
    allOcs = Parallel(n_jobs = num_cores)(delayed(makeDecision)(pr, n) for pr in allOcs)
print((datetime.datetime.now() - t0).total_seconds()/60)

if args.log:
    with open(args.log, 'w') as out:
        for key in log_dict:
            out.write(log_dict[key])
            out.write('\n-----------\n\n')

if args.o:
    print("Writing file")
    allOcs.sort(key = lambda el: el[1])
    newText = ''
    pos = 0

    for pr in allOcs:
        newText += text[pos:pr[1]] + pr[3]
        pos = len(newText)
    newText += text[pos:]

    with open(args.o, 'w') as out:
        out.write(newText)
