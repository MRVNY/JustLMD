import os
import json
import random

if os.path.exists('/home/yiyu/'):
    path = '/home/yiyu/JustLM2D/'
else: path = '/Users/Marvin/NII_Code/JustLM2D/'

import sys
sys.path.insert(0, path + '/Pipeline/')
sys.path.insert(0, path + '/ACTOR/')
from LMD_Dataset import LMD_Dataset

import matplotlib.pyplot as plt
import torch
from src.utils.get_model_and_data import get_model_and_data
from src.parser.visualize import parser
from src.utils.tensors import collate
from src.models.get_model import get_model as get_gen_model

from src.parser.training import parser

parameters = parser()
parameters['device'] = torch.device('cpu')

test_path = path + '/Songs_Test/'
test_dataset = LMD_Dataset(path + '/Pipeline/', [test_path], name='Test')

model = get_gen_model(parameters)
state_dict = torch.load(path + "/ACTOR/exps/0619/checkpoint_5000.pth.tar", map_location='cpu')
model.load_state_dict(state_dict)

seq_name = random.choice(list(test_dataset.indexing.values()))
test_sequence = test_dataset.LMD_Dict[seq_name]
batch = [test_sequence]

batch = collate(batch)
batch['z'] = torch.randn(1, 256)

# inference
model.eval()
batch = model.decoder(batch)
out = batch['output']
out = out[0]
out = out.permute(2,0,1)
out = out.reshape(180,78)

[song, tag] = seq_name.split('_')
torch.save(out,'%s/%s.pt'%(test_path + song, seq_name))


test_dataset.export(seq_name, test_path + seq_name.split('.')[0], inf=True)