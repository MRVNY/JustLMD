import os
import librosa
import json
import datetime
from torch.utils.data import DataLoader, Dataset
import numpy as np
import json
import torch

def toSeconds(time_stamp):
    minutes, seconds = map(float, time_stamp.split(':'))
    return datetime.timedelta(minutes=minutes, seconds=seconds).total_seconds()

#Lyrics_Audio_Dance_Dataset
class LAD_DataSet(Dataset): 
    def __init__ (self, songs_dir):
        self.LAD_Dict = {}
        self.indexing = {}
        index = 0
        
        fps = 25
        sr = 16000
        
        songList = os.listdir(songs_dir)
        for song in songList:
            dir = songs_dir + song
            if song[0] in ['.','_'] or not os.path.isdir(dir):
                continue
            
            print(dir)
            # LYRICS SEQUENCES
            with open('%s/lyrics.lrc'%dir,'r') as fin:
                lines = fin.readlines()
                lines = [line.strip() for line in lines]
            
            # TIMESTAMPS FOR PARSING SEQUENCES
            timestamps = [toSeconds(line.split(']')[0][1:]) for line in lines]
            
            poseDir = '%s/output-smpl-3d/smplfull/'%dir
            audioDir = '%s/audios/'%dir
            
            max_audio_length = 200
            max_dance_length = 500
                    
            # STORE BY SEQUENCE
            for i in range(len(timestamps)):
                tag = str(int(timestamps[i]))
                
                if i == len(timestamps)-1 or \
                    not os.path.exists(audioDir + tag + '.wav') or \
                        not os.path.exists(poseDir+ tag):
                    continue

                # lyrics
                lyrics = lines[i].split(']')[1]

                # audio
                if i == len(timestamps)-1:
                    continue
                
                audio,sr = librosa.load(audioDir + tag + '.wav', sr=sr)
                
                # Extract features (e.g. Mel spectrogram)
                mel_spec = librosa.feature.melspectrogram(y=audio, sr=sr, n_fft=2048, hop_length=512, n_mels=128)
                mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)
                mel_spec_db_norm = (mel_spec_db - np.mean(mel_spec_db)) / np.std(mel_spec_db)
                # Convert to PyTorch tensor
                audio_feat = torch.from_numpy(mel_spec_db_norm)
                audio_feat = torch.nn.functional.pad(audio_feat, pad=(0, max_audio_length - audio_feat.size(1) ), mode='constant', value=0)

                
                # dance
                if i == len(timestamps)-1:
                    continue
                
                dance = []
                for frame in os.listdir(poseDir+ tag):
                    with open(poseDir + tag + '/' + frame) as obj:
                        dance.append(json.load(obj)['annots'][0]['poses'][0])
                
                dance = torch.from_numpy(np.array(dance))
                dance = torch.nn.functional.pad(dance, pad=(0,0,0, max_dance_length - dance.size(0) ), mode='constant', value=0)
                
                # LAD Dict
                tmp = {'lyrics':lyrics, 'audio':audio_feat, 'dance':dance}
                
                self.LAD_Dict[dir+"_"+tag] = tmp
                self.indexing[index] = song+"_"+tag
                index += 1
                
        with open("indexing.json", "w") as json_file:
            json.dump(self.indexing, json_file)

    def __getitem__(self,index):
        key = self.indexing[index]
        item = self.LAD_Dict[key]
        return item['lyrics'], item['audio'], item['dance']
    
    def __len__ (self):
        return len(self.indexing.keys())
    
# dataset = LAD_DataSet('/home/yiyu/JustLMD/Songs/')
# dataloader = DataLoader(dataset=dataset, batch_size=4, shuffle=True, num_workers=2)

# dataiter = iter(dataloader)
# data = next(dataiter)
# print(data)

# torch.save(dataset, 'LMD.pth')

# # dataset = torch.load('my_dataset.pth')
