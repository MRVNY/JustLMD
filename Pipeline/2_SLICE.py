import os
from moviepy.editor import VideoFileClip, AudioFileClip
import re
import librosa
import soundfile as sf
import json
import datetime

fps = 30
sr = 16000

if os.path.exists('/home/yiyu/'):
    path = '/home/yiyu/JustLM2D/'
else: path = '/Users/Marvin/NII_Code/JustLM2D/'

jd2022 = json.load(open(path+"Pipeline/jd2022.json", "r"))

def toSeconds(time_stamp):
    minutes, seconds = map(float, time_stamp.split(':'))
    return datetime.timedelta(minutes=minutes, seconds=seconds).total_seconds()

for song in jd2022.keys():
    song_dir = path+'Songs/'+song
    if song[0]=='.' or song[0]=='_' \
        or not os.path.isdir(song_dir) \
                or not os.path.exists('%s/lyrics.lrc'%(song_dir)):
        continue
    
    if not os.path.exists('%s/videos'%song_dir):
        os.system('mkdir %s/videos'%song_dir)
        os.system('mkdir %s/audios'%song_dir)
        
    if len(os.listdir('%s/videos'%song_dir)) > 0 or len(os.listdir('%s/audios'%song_dir)) > 0:
        continue
    
    # LYRICS SEQUENCES
    with open('%s/lyrics.lrc'%song_dir,'r') as fin:
        lines = fin.readlines()
        if len(lines) == 0:
            continue
        lines = [line.strip() for line in lines]
        if lines[0][0] != '[':
            continue
    
    # AUDIO SEQUENCES
    if not os.path.exists('%s/audio.wav'%song_dir):
        os.system('ffmpeg -i %s/video.mp4 -ab 160k -ac 2 -ar %s -vn %s/audio.wav'%(song_dir, str(sr), song_dir))
    # audioclip = AudioFileClip(song_dir+"/video.mp4")
    # audioclip.write_audiofile(song_dir+"/audio.wav")
    # audioclip.close()
    audios,sr = librosa.load(song_dir+'/audio.wav', sr=sr)
    
    # VIDEO SEQUENCES
    video = VideoFileClip(song_dir+'/video.mp4')
    
    # TIMESTAMPS FOR PARSING SEQUENCES
    timestamps = [toSeconds(line.split(']')[0][1:]) for line in lines]
    
    # STORE BY SEQUENCE
    for i in range(len(timestamps)):
        # lyrics
        lyrics = re.sub(r'\W+', '',lines[i].split(']')[1])

        # audio
        if i == len(timestamps)-1:
            continue
            # audio = audios[int(timestamps[i]*sr) : ]
        else:
            audio = audios[int(timestamps[i]*sr) : int((timestamps[i+1])*sr)]
            sf.write(song_dir+'/audios/'+ str(int(timestamps[i])) + '.wav', audio, sr)
            #slice video
            # os.system('ffmpeg -i %s/video.mp4 -ss %s -to %s -c copy %s/videos/%s.mp4'%(song_dir, str(timestamps[i]), str(timestamps[i+1]), song_dir, str(int(timestamps[i]))))
            video.subclip(timestamps[i], timestamps[i+1]).write_videofile(song_dir+'/videos/'+ str(int(timestamps[i])) + '.mp4', fps=fps, audio=True)
        