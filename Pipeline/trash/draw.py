import datetime
import numpy as np
import os
import json
import logging
from moviepy.editor import *

import cv2
import imageio
import unicodedata

logger = logging.getLogger(__name__)

CANVAS_SIZE = (400,400,3)
videoWriter = None

def toSeconds(time_stamp):
  minutes, seconds = map(float, time_stamp.split(':'))
  return datetime.timedelta(minutes=minutes, seconds=seconds).total_seconds()

def draw(frames, export_to_file=False):
    global CANVAS_SIZE
    global videoWriter
    frames[:,:,0] += CANVAS_SIZE[0]//2
    frames[:,:,1] += CANVAS_SIZE[1]//2
    for i in range(len(frames)):
        cvs = np.ones(CANVAS_SIZE)
        color = (0,0,0)
        hlcolor = (255,0,0)
        dlcolor = (0,0,255)
        for points in frames[i]:
            cv2.circle(cvs,(int(points[0]),int(points[1])),radius=4,thickness=-1,color=hlcolor)
        frame = frames[i]
        cv2.line(cvs, (int(frame[0][0]), int(frame[0][1])), (int(frame[1][0]), int(frame[1][1])), color, 2)	
        cv2.line(cvs, (int((frame[0][0]+frame[1][0])/2), int((frame[0][1]+frame[1][1])/2)), (int((frame[3][0]+frame[12][0])/2), int((frame[3][1]+frame[12][1])/2)), color, 2)
        cv2.line(cvs, (int(frame[3][0]), int(frame[3][1])), (int((frame[3][0]+frame[12][0])/2), int((frame[3][1]+frame[12][1])/2)), color, 2)
        cv2.line(cvs, (int(frame[3][0]), int(frame[3][1])), (int(frame[4][0]), int(frame[4][1])), color, 2)
        cv2.line(cvs, (int(frame[4][0]), int(frame[4][1])), (int(frame[5][0]), int(frame[5][1])), color, 2)
        cv2.line(cvs, (int(frame[5][0]), int(frame[5][1])), (int(frame[6][0]), int(frame[6][1])), color, 2)
        cv2.line(cvs, (int(frame[12][0]), int(frame[12][1])), (int((frame[3][0]+frame[12][0])/2), int((frame[3][1]+frame[12][1])/2)), color, 2)
        cv2.line(cvs, (int(frame[12][0]), int(frame[12][1])), (int(frame[13][0]), int(frame[13][1])), color, 2)
        cv2.line(cvs, (int(frame[13][0]), int(frame[13][1])), (int(frame[14][0]), int(frame[14][1])), color, 2)
        cv2.line(cvs, (int(frame[14][0]), int(frame[14][1])), (int(frame[15][0]), int(frame[15][1])), color, 2)
        cv2.line(cvs, (int(frame[2][0]), int(frame[2][1])), (int((frame[3][0]+frame[12][0])/2), int((frame[3][1]+frame[12][1])/2)), color, 2)
        cv2.line(cvs, (int(frame[2][0]), int(frame[2][1])), (int(frame[7][0]), int(frame[7][1])), color, 2)
        cv2.line(cvs, (int(frame[7][0]), int(frame[7][1])), (int(frame[8][0]), int(frame[8][1])), color, 2)
        cv2.line(cvs, (int(frame[8][0]), int(frame[8][1])), (int(frame[9][0]), int(frame[9][1])), color, 2)
        cv2.line(cvs, (int(frame[9][0]), int(frame[9][1])), (int((frame[10][0]+frame[11][0])/2), int((frame[10][1]+frame[11][1])/2)), color, 2)
        cv2.line(cvs, (int(frame[10][0]), int(frame[10][1])), (int(frame[11][0]), int(frame[11][1])), color, 2)
        cv2.line(cvs, (int(frame[2][0]), int(frame[2][1])), (int(frame[16][0]), int(frame[16][1])), color, 2)
        cv2.line(cvs, (int(frame[16][0]), int(frame[16][1])), (int(frame[17][0]), int(frame[17][1])), color, 2)
        cv2.line(cvs, (int(frame[17][0]), int(frame[17][1])), (int(frame[18][0]), int(frame[18][1])), color, 2)
        cv2.line(cvs, (int(frame[18][0]), int(frame[18][1])), (int((frame[19][0]+frame[20][0])/2), int((frame[19][1]+frame[20][1])/2)), color, 2)
        cv2.line(cvs, (int(frame[19][0]), int(frame[19][1])), (int(frame[20][0]), int(frame[20][1])), color, 2)
        
        if export_to_file:
            img8 = (np.flip(cvs,0)*(2**8-1)).astype(np.uint8)
            videoWriter.append_data(img8)
            
        else:
            cv2.imshow('canvas',np.flip(cvs,0))
            cv2.waitKey(0)
    pass

def exportMP3(name,speed=25):
    global videoWriter
    with open('../%s/config.json'%name) as fin:
        config = json.load(fin)
    print(config)
    with open('../%s/skeletons.json'%name,'r') as fin:
        data = np.array(json.load(fin)['skeletons'])
        
    fontC = 'NotoSansSC-Regular.otf'
    fontK = 'NotoSansKR-Regular.otf'
        
    os.system('rm exports/%s.mp4'%name)
    videoWriter = imageio.get_writer('exports/'+name+'.avi', fps=speed)

    draw(data,export_to_file=True)
    videoWriter.close()
    
    os.system('ffmpeg -i exports/%s.avi exports/%s.mp4'%(name,name))

    #skeleton video
    movie_dance = VideoFileClip('exports/%s.mp4'%name,audio=True)
    
    #music
    movie_music = AudioFileClip('../'+name+'/audio.mp3').subclip(config['start_position']/25, config['end_position']/25)
    movie_dance = movie_dance.set_audio(movie_music)
    
    #lyrics
    with open('../'+name+'/lyrics.lrc','r') as file:
      lyrics = file.readlines()
      lyrics = [line.strip() for line in lyrics]
      font = fontC
      
    toAdd = []
    for i in range(len(lyrics)-1,-1,-1):
      tmp = lyrics[i].split(']')
      if(len(tmp) == 2):
        text = tmp[1]
        if text == '': text = " "
        if font != fontK and 'HANGUL' in unicodedata.name(text[0]): font = fontK
        
        start = toSeconds(tmp[0][1:])
        start = (round(start * 25) - config['start_position'])/25
        
        if(toAdd != []):
          dur = toAdd[-1][1] - start
        else: dur = config['end_position']/25 - start
        
        toAdd.append((text,start,dur))
      
    toAdd.reverse()
      
    clips = [movie_dance]
    for (text,start,dur) in toAdd:
      if(start<0 and start+dur>=0): #if the start of the dance is in the middle of the lyric
        dur += start
        start = 0
      if(start>=0):
        clip = TextClip(text, font=font, fontsize=20, color='black').set_position(('center','bottom')).set_start(start).set_duration(dur)
        clips.append(clip)
    movie_dance = CompositeVideoClip(clips).subclip(0, (config['end_position']-config['start_position'])/25)
  
    #export
    movie_dance.write_videofile("exports/%s.avi"%name,fps=speed,codec='libx264')
    print("exported to avi")

    os.system('rm exports/%s.mp4'%name)
    os.system('ffmpeg -i exports/%s.avi exports/%s.mp4'%(name,name))
    os.system('rm exports/%s.avi'%name)

    logger.info('Finish <%s>'%name)

if __name__ == '__main__':
    name = 'DANCE_C_2'
    # exportMP3(name)
    
    dirs = os.listdir('../')
    for name in dirs:
      print("\n\n\n"+name)
      if name[:5] != 'DANCE' or os.path.exists('exports/%s.mp4'%name):
          continue
      exportMP3(name)
