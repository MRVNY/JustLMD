from multiprocessing import freeze_support
import os
import torch
from torch.utils.data import DataLoader, Dataset

import sys
sys.path.insert(0, '../Baseline/')
from LMD_Dataset import LMD_Dataset, toSeconds

if os.path.exists('/home/yiyu/'):
    path = '/home/yiyu/JustLM2D/'
else: path = '/Users/Marvin/NII_Code/JustLM2D/'

if __name__ == '__main__':
    freeze_support()
    print("HERE0///////////////")
    
    dataset = LMD_Dataset(path+'/Songs/')
    torch.save(dataset, 'LMD.pth')

    # dataset = torch.load('LMD.pth')

    print("HERE2\n\n")
    dataloader = DataLoader(dataset=dataset, batch_size=4, shuffle=True, num_workers=2)

    # print(list(dataloader.dataset.LAD_Dict.items())[0])
    print("HERE3\n\n")
    dataiter = iter(dataloader)
    print("HERE4\n\n")
    data = next(dataiter)
    print("HERE5\n\n")
    print(data)
