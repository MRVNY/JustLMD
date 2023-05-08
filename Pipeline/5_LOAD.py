from multiprocessing import freeze_support
import torch
from torch.utils.data import DataLoader
from GLOBAL import *
import datetime

import sys
sys.path.insert(0, '../Baseline/')
from LMD_Dataset import LMD_Dataset, toSeconds

if __name__ == '__main__':
    freeze_support()
    
    dataset = LMD_Dataset(path+'/Songs/')
    torch.save(dataset, 'LMD_%s.pth'%datetime.datetime.now().strftime("%Y%m%d%H%M%S"))

    # dataset = torch.load('LMD.pth')

    dataloader = DataLoader(dataset=dataset, batch_size=4, shuffle=True, num_workers=2)

    # print(list(dataloader.dataset.LAD_Dict.items())[0])
    dataiter = iter(dataloader)
    data = next(dataiter)
    print(data)
