# clean all the files in every folder of Songs_2022 except video.mp4 .lrc and audio.wav
import os

# remove .DS_Store
os.system('rm -rf %s'%('/Users/Marvin/NII_Code/JustLM2D/Songs_2022/.DS_Store'))

for song in os.listdir('/Users/Marvin/NII_Code/JustLM2D/Songs_2022'):
    for file in os.listdir('/Users/Marvin/NII_Code/JustLM2D/Songs_2022/'+song):
        if file != 'video.mp4' and file != 'lyrics.lrc' and file != 'audio.wav':
            if os.path.isdir('/Users/Marvin/NII_Code/JustLM2D/Songs_2022/'+song+'/'+file):
                os.system('rm -rf %s'%('/Users/Marvin/NII_Code/JustLM2D/Songs_2022/'+song+'/'+file))
            else: os.remove('/Users/Marvin/NII_Code/JustLM2D/Songs_2022/'+song+'/'+file)
