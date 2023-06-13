import os

import matplotlib.pyplot as plt
import torch
from src.utils.get_model_and_data import get_model_and_data
from src.parser.visualize import parser
from src.utils.tensors import collate

from src.parser.training import parser

parameters = parser()
parameters['device'] = torch.device('cpu')

model, datasets = get_model_and_data(parameters)

state_dict = torch.load("/home/yiyu/JustLM2D/ACTOR/exps/saved/checkpoint_5000.pth.tar")
model.load_state_dict(state_dict)

test_sequence = datasets.LAD_Dict['JustDance2022NailsHairHipsHeelsJustDanceVersionbyTodrickHallGameplay_38']
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

