import os
import json
import random

if os.path.exists('/home/yiyu/'):
    path = '/home/yiyu/JustLM2D/'
else: path = '/Users/Marvin/NII_Code/JustLM2D/'

import sys
from LMD_Dataset import LMD_Dataset

import matplotlib.pyplot as plt
import torch
from src.utils.get_model_and_data import get_model_and_data
from src.parser.visualize import parser
from src.utils.tensors import collate

from src.parser.training import parser

parameters = parser()
parameters['device'] = torch.device('cpu')

test_path = path + '/Songs_Test/'
test_dataset = LMD_Dataset(path + '/Pipeline/', [test_path], name='Test')

model, _ = get_model_and_data(parameters)
state_dict = torch.load(path + "/ACTOR/exps/saved/checkpoint_5000.pth.tar", map_location='cpu')
model.load_state_dict(state_dict)

seq_name = random.choice(test_dataset.indexing.keys())
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

torch.save(out, test_path + seq_name+'.pt')


test_dataset.visualize(seq_name, test_path + seq_name.split('.')[0], inf=True)