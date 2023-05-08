from GLOBAL import *

todo = []
for song in jd2022.keys():
    song_path = songs_dir+song
    if song[0]=='.' or song[0]=='_' \
        or not os.path.isdir(song_path) \
            or len(os.listdir('%s/videos'%song_path)) == 0 \
                or len(os.listdir('%s/audios'%song_path)) == 0 \
                    or ( os.path.exists('%s/output-smpl-3d'%(song_path)) and (not os.path.exists('%s/annots'%(song_path)) or len(os.listdir('%s/annots'%(song_path))) == 0)):
        continue
    todo.append(song)

todo.sort()
print(todo)
todo = todo[::-1]

for song in todo:
    song_path = songs_dir+song
    if os.path.exists('%s/output-smpl-3d/smplmesh'%song_path):
        for dir in os.listdir('%s/output-smpl-3d/smplmesh'%song_path):
            os.system('rm -rf %s/images/%s'%(song_path,dir))
            os.system('rm -rf %s/annots/%s'%(song_path,dir))

os.chdir('./.EasyMocap/')

for song in todo:
    song_path = songs_dir+song
    
    os.system('cd .EasyMocap/ | python apps/demo/mocap.py %s --work internet --fps 30 --bodyonly'%song_path) 
    #--disable_vismesh \
    
    if os.path.exists('%s/output-smpl-3d/smplmesh'%song_path):
        for dir in os.listdir('%s/output-smpl-3d/smplmesh'%song_path):
            os.system('rm -rf %s/images/%s'%(song_path,dir))
            os.system('rm -rf %s/annots/%s'%(song_path,dir))
            
for song in os.listdir(path):
    song_path = songs_dir+song
    if os.path.exists('%s/output-smpl-3d'%song_path):
        for dir in os.listdir('%s/output-smpl-3d/smplmesh'%song_path):
            if dir[-4:] == '.mp4':
                # get file name without .mp4
                toDel = dir[:-4]
                os.system('rm -rf %s/output-smpl-3d/smplmesh/%s'%(song_path,toDel))
    if os.path.exists('%s/images'%song_path) and os.path.exists('%s/annots'%song_path)  and os.path.exists('%s/cache_spin'%song_path) \
        and len(os.listdir('%s/images'%song_path)) == 0 and len(os.listdir('%s/annots'%song_path)) == 0:
        os.system('rm -rf %s/images'%song_path)
        os.system('rm -rf %s/annots'%song_path)
        os.system('rm -rf %s/cache_spin'%song_path)
        
for song in os.listdir(path):
    song_path = songs_dir+song
    os.system('rm -rf %s/cache_spin'%song_path)