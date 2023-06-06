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

lyrics_padding = 180

def load_music(audio_path, start):
    audio = librosa.core.load(audio_path, sr=sr, offset=start, duration=sequenceLength)[0]
    
    # Extract features (e.g. Mel spectrogram)
    mel_spec = librosa.feature.melspectrogram(y=audio, sr=sr, hop_length=601, n_mels=128)
    mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)
    mel_spec_db_norm = (mel_spec_db - np.mean(mel_spec_db)) / np.std(mel_spec_db)
    # Convert to PyTorch tensor
    audio_features = torch.from_numpy(mel_spec_db_norm).T
    return audio_features

def load_dance(full_dance, timestamp):
    dance = []
    start = toSeconds(timestamp)*fps
    print(timestamp)
    
    for offset in range(sequenceLength*fps):
        stamp = str(int(start + offset)).zfill(6)
        # print(len(list(full_dance.keys())))
        dance.append(full_dance[stamp]['annots'][0]['poses'][0])
    
    dance = torch.from_numpy(np.array(dance))
    return dance
    
def load_lyrics(lyrics, tokenizer, model):
    tokens = tokenizer.encode_plus(lyrics, add_special_tokens=True, return_tensors='pt')
    outputs = model(**tokens)
    # get the cls token
    lyrics_embeddings = outputs[0][:,0,:]
    lyrics_embeddings = outputs.last_hidden_state[0].detach()
    
    lyrics_embeddings = torch.nn.functional.pad(lyrics_embeddings, pad=(0,0,0,lyrics_padding - lyrics_embeddings.size(0)), mode='constant', value=0)
    return lyrics_embeddings

def init_dataset (songs_collection):
    from GLOBAL import sr, fps, sequenceLength
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertModel.from_pretrained('bert-base-uncased')
    
    LMD_Dict = {}
    indexing = {}
    index = 0
    songs = []
    
    for year_dir in songs_collection:
        for song in os.listdir(year_dir):
            print(song)
            song_path = year_dir + song
            if song[0] in ['.','_'] or not os.path.isdir(song_path):
                continue
            
            if not os.path.exists('%s/audio.wav'%song_path) or \
                not os.path.exists('%s/output-smpl-3d/smplfull.json'%song_path):
                continue
            
            sliced = json.load(open(song_path + '/sliced.json', 'r'))
            
            full_audio,sr = librosa.load('%s/audio.wav'%song_path, sr=sr)
            full_dance = json.load(open('%s/output-smpl-3d/smplfull.json'%song_path, 'r'))
            
            start = list(sliced.keys())[0]
            todo = list(sliced.keys())
            del todo[-1]
            for timestamp in todo:
                trimed_timestamp = toTimestamp(toSeconds(timestamp)-toSeconds(start))
                seconds = toSeconds(timestamp)
                tag = str(int(seconds))
                frame = int(seconds*fps)
                
                # LAD Dict
                tmp = {'lyrics':load_lyrics(sliced[timestamp], tokenizer, model), \
                    'music':load_music('%s/audio.wav'%song_path, seconds), \
                    'dance':load_dance(full_dance, trimed_timestamp)}
                
                LMD_Dict[song+"_"+tag] = tmp
                indexing[index] = song+"_"+tag
                index += 1

    with open("indexing.json", "w", encoding="utf-8") as json_file:
        json.dump(indexing, json_file, ensure_ascii=False, indent=4)
        
    return LMD_Dict
    
if __name__ == '__main__':
    freeze_support()
    
    LMD_Dict = init_dataset(songs_collection)
    torch.save(LMD_Dict, 'JD20-22_LMD_Dict_%s.pth'%datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
    
    # LMD_Dict = torch.load('JD2021_LMD_Dict_20230602181139.pth')
    indexing = json.load(open("indexing.json", 'r'))
    
    sample = LMD_Dict['JustDance2021YOUVEGOTAFRIENDINMEDisneyPixarsToyStoryCosplayGameplay_18']

    dataset = LMD_Dataset(LMD_Dict, indexing)
    # torch.save(dataset, 'LMD_%s.pth'%datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
    # dataset = torch.load('LMD.pth')

    dataloader = DataLoader(dataset=dataset, batch_size=4, shuffle=True, num_workers=1)

    # print(list(dataloader.dataset.LMD_Dict.items())[0])
    dataiter = iter(dataloader)
    data = next(dataiter)
    print(data['lyrics'].size(), data['music'].size(), data['dance'].size())
