from modules import *
from path import chapterPath

chapter = readL(chapterPath)['settingList']
data = chapter[0]['rows']
name = ''
res = {}
for each in data:
    idx = each['rowIndex']
    if idx < 3:
        continue
    string = each['strings']
    if len(string) < 3:
        continue
    if string[0] == 'Yes':
        break
    res[string[0]] = string[2]

res['？？？'] = '？？？'

writeD('data/names.json', res)
#writeR('data/names.txt', str(res))
