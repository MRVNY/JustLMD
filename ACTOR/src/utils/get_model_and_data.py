import os
import json
import torch
from ..datasets.get_dataset import get_datasets
from ..recognition.get_model import get_model as get_rec_model
from ..models.get_model import get_model as get_gen_model
from src.datasets.LMD_Dataset import LMD_Dataset



def get_model_and_data(parameters):
    # datasets = get_datasets(parameters)
    if os.path.exists('/home/yiyu/JustLM2D/Pipeline/JD20-22_LMD_Dict_20230602192541.pth'):
        LMD_Dict = torch.load('/home/yiyu/JustLM2D/Pipeline/JD20-22_LMD_Dict_20230602192541.pth')
        indexing = json.load(open("/home/yiyu/JustLM2D/Pipeline/indexing.json", 'r', encoding="utf-8"))
        datasets = LMD_Dataset(LMD_Dict, indexing)
    else: datasets = None

    if parameters["modelname"] == "recognition":
        model = get_rec_model(parameters)
    else:
        model = get_gen_model(parameters)
    return model, datasets
