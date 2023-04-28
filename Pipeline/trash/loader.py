import datetime
import json
import os
import torch
import librosa
from torch.utils.data import DataLoader, Dataset
import numpy as np
import math 

LYRICS = 0
AUDIO = 1
DANCE = 2

def toSeconds(time_stamp):
  minutes, seconds = map(float, time_stamp.split(':'))
  return datetime.timedelta(minutes=minutes, seconds=seconds).total_seconds()

#Lyrics_Audio_Dance_Dataset
class LAD_DataSet(Dataset): 
  def __init__ (self):
    self.LAD_Dict = {}
    self.indexing = {}
    index = 0
    
    fps = 25
    sr = 16000
    
    self.dirs = os.listdir('../')
    for dir in self.dirs:
      if dir[:5] != 'DANCE':
        self.dirs.remove(dir)

      else:
        with open('../%s/config.json'%dir) as fin:
          config = json.load(fin)
          start = config['start_position']/fps
          end = config['end_position']/fps
        
        # LYRICS SEQUENCES
        with open('../%s/lyrics.lrc'%dir,'r') as fin:
          lines = fin.readlines()
          lines = [line.strip() for line in lines]
        # lines = np.loadtxt('../'+dir+'/lyrics.lrc', delimiter="\n", dtype=str)
        
        # DANCE SEQUENCES
        with open('../%s/skeletons.json'%dir,'r') as fin:
          choreos = np.array(json.load(fin)['skeletons'])
        
        # AUDIO SEQUENCES
        audios,sr = librosa.load('../'+dir+'/audio.mp3', sr=sr)
        
        # TIMESTAMPS FOR PARSING SEQUENCES
        timestamps = [toSeconds(line.split(']')[0][1:]) for line in lines]
        
        # STORE BY SEQUENCE
        for i in range(len(timestamps)):
          # lyrics
          lyrics = lines[i].split(']')[1]
          # lyrics = torch.tensor(list(lyrics.encode()))

          # audio
          if i == len(timestamps)-1:
            audio = audios[int(timestamps[i]*sr) : int(end*sr)]
          else:
            audio = audios[int(timestamps[i]*sr) : int((timestamps[i]+1)*sr)]
          
          # Extract features (e.g. Mel spectrogram)
          mel_spec = librosa.feature.melspectrogram(y=audio, sr=sr, n_fft=2048, hop_length=512, n_mels=128)
          mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)
          mel_spec_db_norm = (mel_spec_db - np.mean(mel_spec_db)) / np.std(mel_spec_db)
          # Convert to PyTorch tensor
          audio_feat = torch.tensor(mel_spec_db_norm).float()
          
          # dance
          if i == len(timestamps)-1:
            dance = choreos[int(timestamps[i]*fps) : int(end*fps)]
          else:
            dance = choreos[int(timestamps[i]*fps) : int((timestamps[i]+1)*fps)]

          dance = torch.from_numpy(dance)
          
          tmp = {'lyrics':lyrics, 'audio':audio_feat, 'dance':dance}
          
          self.LAD_Dict[dir+"_"+str(timestamps[i])] = tmp
          self.indexing[index] = dir+"_"+str(timestamps[i])
          index += 1
          
    with open("indexing.json", "w") as json_file:
      json.dump(self.indexing, json_file)

  def __getitem__(self,index):
    key = self.indexing[index]
    item = self.LAD_Dict[key]
    return item['lyrics'], item['audio'], item['dance']
  
  def __len__ (self):
    return len(self.indexing.keys())

if __name__ == '__main__':
  dataset = LAD_DataSet()
  dataloader = DataLoader(dataset=dataset, batch_size=4, shuffle=True, num_workers=2)

  dataiter = iter(dataloader)
  data = dataiter.next()
  print(data)