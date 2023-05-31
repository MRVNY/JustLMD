import os
import json

if os.path.exists('/home/yiyu/'):
    path = '/home/yiyu/JustLM2D/'
else: path = '/Users/Marvin/NII_Code/JustLM2D/'

# jd2022 = json.load(open(path + "/Pipeline/jd2022.json", "r"))
jd2022 = {'SweetButPsychoAvaMaxJustDance2023Edition':[]}

year = '2022'
# songs_dir = path+'Songs/'
songs_dir = path + 'Songs_'+year+'/'

fps = 30
sr = 16000
sequenceLength = 6

version = 'JD'+year

def getSongList(version):
    if not os.path.exists(version+".json"):
        songList = {}
        json.dump(songList, open(version+".json", "w", encoding="utf-8"), ensure_ascii=False, indent=4)

    songList = json.load(open(version+".json", "r"))
    return songList
