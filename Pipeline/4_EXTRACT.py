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
print(todo)
todo = todo[::-1]

for song in todo:
    song_dir = path+song
    if os.path.exists('%s/output-smpl-3d/smplmesh'%song_dir):
        for dir in os.listdir('%s/output-smpl-3d/smplmesh'%song_dir):
            os.system('rm -rf %s/images/%s'%(song_dir,dir))
            os.system('rm -rf %s/annots/%s'%(song_dir,dir))

os.chdir('./.EasyMocap/')

for song in todo:
    song_dir = path+song
    
    os.system('cd .EasyMocap/ | python apps/demo/mocap.py %s --work internet --fps 30 --bodyonly'%song_dir) 
    #--disable_vismesh \
    
    if os.path.exists('%s/output-smpl-3d/smplmesh'%song_dir):
        for dir in os.listdir('%s/output-smpl-3d/smplmesh'%song_dir):
            os.system('rm -rf %s/images/%s'%(song_dir,dir))
            os.system('rm -rf %s/annots/%s'%(song_dir,dir))
            
for song in os.listdir(path):
    song_dir = path+song
    if os.path.exists('%s/output-smpl-3d'%song_dir):
        for dir in os.listdir('%s/output-smpl-3d/smplmesh'%song_dir):
            if dir[-4:] == '.mp4':
                # get file name without .mp4
                toDel = dir[:-4]
                os.system('rm -rf %s/output-smpl-3d/smplmesh/%s'%(song_dir,toDel))
    if os.path.exists('%s/images'%song_dir) and os.path.exists('%s/annots'%song_dir)  and os.path.exists('%s/cache_spin'%song_dir) \
        and len(os.listdir('%s/images'%song_dir)) == 0 and len(os.listdir('%s/annots'%song_dir)) == 0:
        os.system('rm -rf %s/images'%song_dir)
        os.system('rm -rf %s/annots'%song_dir)
        os.system('rm -rf %s/cache_spin'%song_dir)
        
for song in os.listdir(path):
    song_dir = path+song
    os.system('rm -rf %s/cache_spin'%song_dir)