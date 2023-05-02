import pytube
import os
from moviepy.editor import VideoFileClip, AudioFileClip
import re
import librosa
import soundfile as sf
import json

urls = [
    # ['https://www.youtube.com/watch?v=XLbhUWJZaoc&ab_channel=Dancepool' ,'full'],
    # ['https://www.youtube.com/watch?v=zothFqRuFWY&ab_channel=littlesiha' ,'full'],
    # ['https://www.youtube.com/watch?v=cY7G9IophMc&ab_channel=littlesiha' ,'full'],
    # ['https://www.youtube.com/watch?v=vcJ3ru2C3tY&ab_channel=JustDancersLima' ,'left'],
    # ['https://www.youtube.com/watch?v=_XnjdzhHAXg&ab_channel=Astylia' ,'full'],
    # ['https://www.youtube.com/watch?v=yWtgWgiE6Mw&ab_channel=littlesiha' ,'full'],
    # ['https://www.youtube.com/watch?v=AhzoE39ry-c&ab_channel=littlesiha' ,'full'],
    # ['https://www.youtube.com/watch?v=dsMh40sCn38&ab_channel=littlesiha' ,'full'],
    # ['https://www.youtube.com/watch?v=RiWyqMxlXHI&ab_channel=littlesiha' ,'full'],
    # ['https://www.youtube.com/watch?v=xwnaIFbVWyE&ab_channel=littlesiha' ,'full'],
    # ['https://www.youtube.com/watch?v=sH7DAbJ5VtY&ab_channel=JustDancersLima' ,'left'],
    # ['https://www.youtube.com/watch?v=HHv9EE6jo_4&ab_channel=JustAsh' ,'left'],
    # ['https://www.youtube.com/watch?v=1tEX38jOexQ&ab_channel=ArianaKatana' ,'full'],
    # ['https://www.youtube.com/watch?v=sRP0w3ooKqM&ab_channel=littlesiha' ,'full'],
    # ['https://www.youtube.com/watch?v=aUtl2wcEbg8&ab_channel=littlesiha' ,'full'],
    # ['https://www.youtube.com/watch?v=GWFcOLhjud4&ab_channel=littlesiha' ,'full'],
    # ['https://www.youtube.com/watch?v=luYaccu2g4g&ab_channel=littlesiha' ,'center'],
    # ['https://www.youtube.com/watch?v=r6V_CqzRP3Q&ab_channel=PercentOregon15Gameplay' ,'full'],
    # ['https://www.youtube.com/watch?v=zUInB2dfYuU&ab_channel=littlesiha' ,'full'],
    # ['https://www.youtube.com/watch?v=jBYWd5_4z5E&ab_channel=xTzSharkDance' ,'left'],
    # ['https://www.youtube.com/watch?v=jBYWd5_4z5E&ab_channel=xTzSharkDance' ,'full'],
    # ['https://www.youtube.com/watch?v=KQ2gjEy1QJ8&ab_channel=GiovyGames' ,'full'],
    # ['https://www.youtube.com/watch?v=hmHfCn7JwYo&ab_channel=Dancepool' ,'full'],
    # ['https://www.youtube.com/watch?v=lxbobuEbNLw&ab_channel=KelvinJaeder' ,'center'],
    # ['https://www.youtube.com/watch?v=T0P9-IbF27Q&ab_channel=littlesiha' ,'full'],
    # ['https://www.youtube.com/watch?v=8VLbOLkWrPo&ab_channel=littlesiha' ,'full'],
    # ['https://www.youtube.com/watch?v=b337vhndUK8&ab_channel=JustAsh' ,'left'],
    # ['https://www.youtube.com/watch?v=2G4GAv4rk4Y&ab_channel=JustAsh' ,'full'],
    # ['https://www.youtube.com/watch?v=-UEqa9LeBX0&ab_channel=AsaDreams' ,'center'],
    # ['https://www.youtube.com/watch?v=yZbIE1TZgWM&ab_channel=JustDancersLima' ,'left'],
    # ['https://www.youtube.com/watch?v=du-zvFRqh7U&ab_channel=littlesiha' ,'full'],
    # ['https://www.youtube.com/watch?v=TqAqOCpFvek&ab_channel=KelvinJaeder' ,'center'],
    # ['https://www.youtube.com/watch?v=YS-aMLs1eak&ab_channel=littlesiha' ,'full'],
    # ['https://www.youtube.com/watch?v=uxSFj9KOGrg&ab_channel=littlesiha' ,'full'],
    # ['https://www.youtube.com/watch?v=L2gXOJ5oNfM&ab_channel=Diez' ,'center'],
    # ['https://www.youtube.com/watch?v=f51BwXVGO8Q&ab_channel=Astylia' ,'full'],
    # ['https://www.youtube.com/watch?v=UJWgSP8AJDg&ab_channel=ArianaKatana' ,'full']
    ]

#crop: left, right, center, full
fps = 30
sr = 16000


# Get name and resgister as json
if not os.path.exists("jd2022.json"):
    jd2022 = {}
    json.dump(jd2022, open("jd2022.json", "w"))

jd2022 = json.load(open("jd2022.json", "r"))

finished = jd2022.values()
print(finished)

for url in urls:
    if url in finished:
        print("skipping")
        continue
    yt = pytube.YouTube(url[0])
    print(url)
    jd2022[re.sub(r'\W+', '',yt.title)] = url
    json.dump(jd2022, open("jd2022.json", "w"))

jd2022 = json.load(open("jd2022.json", "r"))
for song in jd2022.keys():
    print(song)
    path = "../Songs/" + re.sub(r'\W+', '',song)
    
    # Audio
    if not os.path.exists(path+"/video.mp4"):
        url = jd2022[song][0]
        crop = jd2022[song][1]
        yt = pytube.YouTube(url)
        print(yt.title)
        
        # audio = yt.streams.get_audio_only()
        # audio.download(output_path=path, filename="audio.mp4")
        
        # audioClip = AudioFileClip(path+"/audio.mp4", fps=fps)

        # # # Extract the audio from the video
        # # audioClip = videoClip.audio

        # # # Write the audio to an MP3 file
        # audioClip.write_audiofile(path+"/audio.mp3")

        # # Close the video and audio files
        # # videoClip.close()
        # audioClip.close()
        
    # else:
    #     audio,sr = librosa.load(path+"/audio.mp3", sr=sr)
    #     audio = audio[0:]
    #     sf.write(path+"/audio2.mp3", audio, sr)
    
        video = yt.streams.get_by_resolution("720p")
        video.download(output_path=path, filename="video.mp4")
        
        os.system('ffmpeg -i %s/video.mp4 -ab 160k -ac 2 -ar %s -vn %s/audio.wav'%(path, str(sr), path))
    
        # Crop 
        if crop != "full":
            os.system('mv %s/video.mp4 %s/tmp.mp4'%(path,path))
            if crop == "left":
                os.system('ffmpeg -i %s/tmp.mp4 -filter:v "crop=in_w/2:in_h:0:0" %s/video.mp4'%(path,path))
            elif crop == "right":
                os.system('ffmpeg -i %s/tmp.mp4 -filter:v "crop=in_w/2:in_h:in_w/2:0" %s/video.mp4'%(path,path))
            elif crop == "center":
                os.system('ffmpeg -i %s/tmp.mp4 -filter:v "crop=in_w/2:in_h:in_w/4:0" %s/video.mp4'%(path,path))
            os.system('rm %s/tmp.mp4'%path)
        
    if not os.path.exists(path+"/lyrics.lrc"):
        os.system('touch '+path+'/lyrics.lrc')