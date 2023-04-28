import os
import json

fps = 30
sr = 16000
jd2022 = json.load(open("/home/yiyu/JustLMD/Pipeline/jd2022.json", "r"))

path = '/home/yiyu/JustLMD/Songs/'

todo = []
for song in jd2022.keys():
    song_dir = path+song
    if song[0]=='.' or song[0]=='_' \
        or not os.path.isdir(song_dir) \
            or len(os.listdir('%s/videos'%song_dir)) == 0 \
                or len(os.listdir('%s/audios'%song_dir)) == 0 \
                    or ( os.path.exists('%s/output-smpl-3d'%(song_dir)) and (not os.path.exists('%s/annots'%(song_dir)) or len(os.listdir('%s/annots'%(song_dir))) == 0)):
        continue
    todo.append(song)

todo.sort()
# todo = todo[::-1]
print(todo)

os.chdir('./.EasyMocap/')
for song in todo:
    song_dir = path+song
    os.system('python apps/preprocess/extract_keypoints.py %s --mode mp-pose'%song_dir)