from modules import *
from path import chapterPath

chapter = readL(chapterPath)['settingList']
data = chapter[2]['rows']
name = ''
res = {}
for each in data:
    idx = each['rowIndex']
    if idx < 3:
        continue
    string = each['strings']
    if string == []:
        continue
    if string[0]:
        name = string[0]
        res[name] = {}
    res[name][string[2]] = string[9].split('/')[1]

writeD('data/chars.json', res)
