from multiprocessing import freeze_support
import os
import torch
from torch.utils.data import DataLoader, Dataset

import sys
sys.path.insert(0, '../Baseline/')
from LMD_Dataset import LMD_Dataset, toSeconds

print("HERE0\n\n")
freeze_support()

# dataset = LMD_Dataset(path+'/Songs/')
# torch.save(dataset, 'LMD.pth')

dataset = torch.load('LMD.pth')

print("HERE2\n\n")
dataloader = DataLoader(dataset=dataset, batch_size=1, shuffle=True, num_workers=1)

print("HERE3\n\n")
dataiter = iter(dataloader)
print("HERE4\n\n")
data = next(dataiter)
print("HERE5\n\n")
print(data)

# dataset = torch.load('my_dataset.pth')
