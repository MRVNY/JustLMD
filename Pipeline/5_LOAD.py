from GLOBAL import *
from multiprocessing import freeze_support
import torch
from torch.utils.data import DataLoader, Dataset
import librosa
import numpy as np

import sys
sys.path.insert(0, '../Baseline/')
from LMD_Dataset import LMD_Dataset

# use DistilBERT
from transformers import BertTokenizer, BertModel

def load_music(full_audio, start):
    audio = librosa.load(full_audio, sr=sr, offset=start, duration=sequenceLength)[0]
    
    # Extract features (e.g. Mel spectrogram)
    mel_spec = librosa.feature.melspectrogram(y=audio, sr=sr, n_fft=2048, hop_length=512, n_mels=128)
    mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)
    mel_spec_db_norm = (mel_spec_db - np.mean(mel_spec_db)) / np.std(mel_spec_db)
    # Convert to PyTorch tensor
    audio_feat = torch.from_numpy(mel_spec_db_norm).type(torch.FloatTensor)
    return

def load_dance(full_dance, start):
    dance = []
    for frame in range(start, start+sequenceLength*fps):
        with open(poseDir + tag + '/' + frame) as obj:
            dance.append(json.load(obj)['annots'][0]['poses'][0])
    
    dance = torch.from_numpy(np.array(dance)).type(torch.FloatTensor)
    return
    
def load_lyrics(string):
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertModel.from_pretrained('bert-base-uncased')
    
    # lyrics
    lyrics = lines[i].split(']')[1]
    tokens = tokenizer.encode_plus(lyrics, add_special_tokens=True, return_tensors='pt')
    outputs = model(**tokens)
    # get the cls token
    lyrics_embeddings = outputs[0][:,0,:]
    lyrics_embeddings = outputs.last_hidden_state[0].T.detach().type(torch.FloatTensor)
    
    return

def init_dataset (self, songs_dir):
    self.LMD_Dict = {}
    self.indexing = {}
    index = 0
        
    for song in os.listdir(songs_dir):
        song_path = songs_dir + song
        if song[0] in ['.','_'] or not os.path.isdir(song_path):
            continue
        
        if not os.path.exists('%s/audio.wav'%song_path) or \
            not os.path.exists('%s/output-smpl-3d/smplfull.json'%song_path):
            continue
        
        sliced = json.load(open(song_path + '/sliced.json', 'r'))
        
        full_audio,sr = librosa.load('%s/audio.wav'%song_path, sr=sr)
        full_dance = json.load(open('%s/output-smpl-3d/smplfull.json'%song_path, 'r'))
        
        for timestamp in list(sliced.keys()):
            tag = str(int(timestamp))
            frame = int(timestamp*fps)
            
            # LAD Dict
            tmp = {'lyrics':load_lyrics(sliced[timestamp]), 'music':load_music(full_audio, frame), 'dance':load_dance(full_dance, frame)}
            
            self.LMD_Dict[song+"_"+tag] = tmp
            self.indexing[index] = song+"_"+tag
            index += 1
            
    with open("indexing.json", "w", encoding="utf-8") as json_file:
        json.dump(self.indexing, json_file, ensure_ascii=False, indent=4)
        
    
if __name__ == '__main__':
    freeze_support()
    
    dataset = LMD_Dataset(path+'/Songs/')
    torch.save(dataset, 'LMD_%s.pth'%datetime.datetime.now().strftime("%Y%m%d%H%M%S"))

    # dataset = torch.load('LMD.pth')

    dataloader = DataLoader(dataset=dataset, batch_size=4, shuffle=True, num_workers=2)

    # print(list(dataloader.dataset.LMD_Dict.items())[0])
    dataiter = iter(dataloader)
    data = next(dataiter)
    print(data)
