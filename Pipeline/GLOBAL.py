import os
import json

if os.path.exists('/home/yiyu/'):
    path = '/home/yiyu/JustLM2D/'
else: path = '/Users/Marvin/NII_Code/JustLM2D/'

# jd2022 = json.load(open(path + "/Pipeline/jd2022.json", "r"))
jd2022 = {'SweetButPsychoAvaMaxJustDance2023Edition':[]}

# songs_dir = path+'Songs/'
songs_dir = path + 'Test/'

fps = 30
sr = 16000