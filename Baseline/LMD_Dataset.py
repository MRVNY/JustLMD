import os
import librosa
import json
import datetime
import torch
from torch.utils.data import Dataset
import numpy as np
import json
import torch

# use DistilBERT
from transformers import BertTokenizer, BertModel

def toSeconds(time_stamp):
    minutes, seconds = map(float, time_stamp.split(':'))
    return datetime.timedelta(minutes=minutes, seconds=seconds).total_seconds()

#Lyrics_Music_Dance_Dataset
class LMD_Dataset(Dataset): 
    def __init__ (self, songs_dir):
        # use DistilBERT
        tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        model = BertModel.from_pretrained('bert-base-uncased')

        self.LAD_Dict = {}
        self.indexing = {}
        index = 0
        
        sr = 16000
        
        songList = os.listdir(songs_dir)
        for song in songList:
            dir = songs_dir + song
            if song[0] in ['.','_'] or not os.path.isdir(dir):
                continue
            
            print(song)
            # LYRICS SEQUENCES
            with open('%s/lyrics.lrc'%dir,'r') as fin:
                lines = fin.readlines()
                lines = [line.strip() for line in lines]
            
            # TIMESTAMPS FOR PARSING SEQUENCES
            timestamps = [toSeconds(line.split(']')[0][1:]) for line in lines]
            
            poseDir = '%s/output-smpl-3d/smplfull/'%dir
            audioDir = '%s/audios/'%dir
            
            max_audio_length = 600
            max_dance_length = 600
            max_lyrics_length = 50
                    
            # STORE BY SEQUENCE
            max_audio = 0
            max_dance = 0
            max_lyrics = 0
            
            for i in range(len(timestamps)):
                tag = str(int(timestamps[i]))
                
                if i == len(timestamps)-1 or \
                    not os.path.exists(audioDir + tag + '.wav') or \
                        not os.path.exists(poseDir+ tag):
                    continue

                # lyrics
                lyrics = lines[i].split(']')[1]
                tokens = tokenizer.encode_plus(lyrics, add_special_tokens=True, return_tensors='pt')
                outputs = model(**tokens)
                # get the cls token
                lyrics_embeddings = outputs[0][:,0,:]
                lyrics_embeddings = outputs.last_hidden_state[0].T.detach().type(torch.FloatTensor)
                if lyrics_embeddings.size(1) > max_lyrics: max_lyrics = lyrics_embeddings.size(1)
                # [22, 768] to [50, 768]
                lyrics_embeddings = torch.nn.functional.pad(lyrics_embeddings, pad=(0, max_lyrics_length - lyrics_embeddings.size(1)), mode='constant', value=0)

                # audio
                if i == len(timestamps)-1:
                    continue
                
                audio,sr = librosa.load(audioDir + tag + '.wav', sr=sr)
                
                # Extract features (e.g. Mel spectrogram)
                mel_spec = librosa.feature.melspectrogram(y=audio, sr=sr, n_fft=2048, hop_length=512, n_mels=128)
                mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)
                mel_spec_db_norm = (mel_spec_db - np.mean(mel_spec_db)) / np.std(mel_spec_db)
                # Convert to PyTorch tensor
                audio_feat = torch.from_numpy(mel_spec_db_norm).type(torch.FloatTensor)
                if audio_feat.size(1) > max_audio: max_audio = audio_feat.size(1)
                audio_feat = torch.nn.functional.pad(audio_feat, pad=(0, max_audio_length - audio_feat.size(1) ), mode='constant', value=0)
                
                # dance
                if i == len(timestamps)-1:
                    continue
                
                dance = []
                for frame in os.listdir(poseDir+ tag):
                    with open(poseDir + tag + '/' + frame) as obj:
                        dance.append(json.load(obj)['annots'][0]['poses'][0])
                
                dance = torch.from_numpy(np.array(dance)).type(torch.FloatTensor)
                if max_dance < dance.size(0): max_dance = dance.size(0)
                dance = torch.nn.functional.pad(dance, pad=(0,0,0, max_dance_length - dance.size(0) ), mode='constant', value=0)
                
                # LAD Dict
                tmp = {'lyrics':lyrics_embeddings, 'music':audio_feat, 'dance':dance}
                
                self.LAD_Dict[song+"_"+tag] = tmp
                self.indexing[index] = song+"_"+tag
                index += 1
                
        with open("indexing.json", "w", encoding="utf-8") as json_file:
            json.dump(self.indexing, json_file, ensure_ascii=False, indent=4)
            
        print("max_audio: ", max_audio, "max_dance: ", max_dance, "max_lyrics: ", max_lyrics)

    def __getitem__(self,index):
        key = self.indexing[index]
        item = self.LAD_Dict[key]
        return item#['lyrics'], item['music'], item['dance']
    
    def __len__ (self):
        return len(self.indexing.keys())