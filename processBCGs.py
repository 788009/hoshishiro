from modules import *
from path import chapterPath

chapter = readL(chapterPath)['settingList']
data = chapter[4]['rows']
res = {}
for each in data:
    idx = each['rowIndex']
    if idx < 1:
        continue
    string = each['strings']
    if string == []:
        continue
    res[string[0]] = string[8]

writeD('data/BCGs.json', res)
