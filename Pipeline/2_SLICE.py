import pytube
import os
from moviepy.editor import VideoFileClip, AudioFileClip
import re
import librosa
import soundfile as sf
import json
import datetime

fps = 30
sr = 16000
jd2022 = json.load(open("jd2022.json", "r"))

def toSeconds(time_stamp):
    minutes, seconds = map(float, time_stamp.split(':'))
    return datetime.timedelta(minutes=minutes, seconds=seconds).total_seconds()

for song in jd2022.keys():
    song_dir = '../Songs/'+song
    if song[0]=='.' or song[0]=='_' \
        or not os.path.isdir(song_dir) \
            or os.path.exists('%s/output-smpl-3d'%(song_dir)) \
                or not os.path.exists('%s/lyrics.lrc'%(song_dir)) :
        continue
    
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
    
    # AUDIO SEQUENCES
    audios,sr = librosa.load(song_dir+'/audio.mp3', sr=sr)
    
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
            
            video.subclip(timestamps[i], timestamps[i+1]).write_videofile(song_dir+'/videos/'+ str(int(timestamps[i])) + '.mp4', fps=fps, audio=True)
        