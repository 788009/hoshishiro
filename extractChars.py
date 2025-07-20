from modules import *
from path import bookPath, BCGsPath, charsPath, namesPath

def getPic(rows, idx):
    res = {}
    strings = rows[idx]['strings']
    if strings[2] == '<Off>':
        res['type'] = 'bg'
    elif '=' in strings[2] and strings[2].split('>')[1]:
        res['type'] = 'normal'
        res['char'] = strings[2].split('=')[1].split('>')[0]
        res['illust'] = chars[res['char']][strings[2].split('=')[1].split('>')[1]].replace('jpg', 'png')
        #print(res['char'], res['illust'])
    elif strings[2] and '=' not in strings[2]:
        res['type'] = 'normal'
        res['char'] = strings[1]
        try:
            res['illust'] = chars[res['char']][strings[2]]
        except:
            print(2, idx, strings, res)
    while rows[idx]['strings'][0] not in ['Bg', 'BgEvent']:
        strings = rows[idx]['strings']
        if len(strings) < 8:
            continue
        if res == {} and target in strings[1] and strings[0] == '' and strings[-2] == '' and strings[2] and 'MessageWindow' not in strings:
            res['type'] = 'normal'
            res['char'] = strings[1]
            try:
                res['illust'] = chars[res['char']][strings[2]].replace('jpg', 'png')
            except:
                try:
                    res['illust'] = chars[res['char']][strings[2].split('=')[1].split('>')[1]].replace('jpg', 'png')
                except:
                    print(1, idx, strings)
                #input()
        idx -= 1
    strings = rows[idx]['strings']
    if strings[0] == 'Bg':
        if not res:
            res['type'] = 'bg'
        res['bg'] = BCGs[strings[1]].replace('jpg', 'png')
    else: # BgEvent
        res['type'] = 'cg'
        res['cg'] = BCGs[strings[1]].replace('jpg', 'png')
    return res

book = readL(bookPath)['importGridList']
BCGs = readL(BCGsPath)
chars = readL(charsPath)
names = readL(namesPath)
target = 'カルハ' #'ねり'
tgtEng = 'karuha' #'neri'
res = []
s = ''
for data in book:
    rows = data['rows']
    for row in rows:
        idx = row['rowIndex']
        strings = row['strings']
        if len(strings) < 13:
            continue
        if tgtEng in strings[10]:
            pic = getPic(rows, idx)
            try:
                char = names[strings[1].replace('大', '')]
            except:
                print(strings[1])
            chs = strings[12] \
                  .replace('<dash=2>', '——') \
                  .replace('<dash=4>', '————') \
                  .replace('<dash=6>', '——————') \
                  .replace('<dash=12>', '————————————')
            jp = strings[8] \
                  .replace('<dash=2>', '——') \
                  .replace('<dash=4>', '————') \
                  .replace('<dash=6>', '——————') \
                  .replace('<dash=12>', '————————————')
            voice = strings[10].split('/')[1].replace('ogg', 'wav')
            #chs = chs.replace('\n', '')
            s += f'{voice} {chs}\n'
            res.append({
                    'pic': pic,
                    'char': char,
                    'chs': chs,
                    'jp': jp,
                    'voice': voice
                })

writeD(f'data/{tgtEng}.json', res)
#writeR(f'data/{tgtEng}.txt', str(res))
#writeR('res.txt', s)
            






