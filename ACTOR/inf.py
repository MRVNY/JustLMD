import os
import json
from LMD_Dataset import LMD_Dataset

import matplotlib.pyplot as plt
import torch
from src.utils.get_model_and_data import get_model_and_data
from src.parser.visualize import parser
from src.utils.tensors import collate

from src.parser.training import parser

parameters = parser()
parameters['device'] = torch.device('cpu')

model, datasets = get_model_and_data(parameters)

LMD_Dict = torch.load('/Users/Marvin/NII_Code/JustLM2D/Pipeline/Test_LMD_Dict_20230613211934.pth')
indexing = json.load(open("/Users/Marvin/NII_Code/JustLM2D/Pipeline/test_indexing.json", 'r', encoding="utf-8"))
datasets = LMD_Dataset(LMD_Dict, indexing)

state_dict = torch.load("/Users/Marvin/NII_Code/JustLM2D/ACTOR/exps/saved/checkpoint_5000.pth.tar", map_location='cpu')
model.load_state_dict(state_dict)

test_sequence = datasets.LAD_Dict['AllTheStarsbyKendrickLamarftSZAJustDance2021_46']
batch = [test_sequence]

batch = collate(batch)
batch['z'] = torch.randn(1, 256)

# inference
# device
model.eval()
batch = model.decoder(batch)
out = batch['output']

out = out[0]
# from size(24,3,180) to (180,24,3)
out = out.permute(2,0,1)
print(out.shape)
print("HERE")
# (180,24,3) to (180,72)
out = out.reshape(180,72)
print(out.shape)

torch.save(out, 'inf.pt')

