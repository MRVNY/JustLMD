import os
import json
import torch
from ..datasets.get_dataset import get_datasets
from ..recognition.get_model import get_model as get_rec_model
from ..models.get_model import get_model as get_gen_model
from LMD_Dataset import *



def get_model_and_data(parameters):
    # datasets = get_datasets(parameters)
    # if os.path.exists(home_path + 'Pipeline/JD20-22_LMD_Dict_20230602192541.pth'):
    #     LMD_Dict = torch.load(home_path + 'Pipeline/JD20-22_LMD_Dict_20230602192541.pth')
    #     indexing = json.load(open(home_path + "Pipeline/indexing.json", 'r', encoding="utf-8"))
    #     datasets = LMD_Dataset(LMD_Dict, indexing)
    # else: datasets = None

    datasets = LMD_Dataset('')

    if parameters["modelname"] == "recognition":
        model = get_rec_model(parameters)
    else:
        model = get_gen_model(parameters)
    return model, datasets
