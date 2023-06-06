import json
import torch
from ..datasets.get_dataset import get_datasets
from ..recognition.get_model import get_model as get_rec_model
from ..models.get_model import get_model as get_gen_model
from src.datasets.LMD_Dataset import LMD_Dataset



def get_model_and_data(parameters):
    # datasets = get_datasets(parameters)
    LMD_Dict = torch.load('/Users/Marvin/NII_Code/JustLM2D/ACTOR/data/HumanAct12Poses/JD20-22_LMD_Dict_20230602192541.pth')
    indexing = json.load(open("/Users/Marvin/NII_Code/JustLM2D/ACTOR/data/HumanAct12Poses/indexing.json", 'r'))
    datasets = LMD_Dataset(LMD_Dict, indexing)

    if parameters["modelname"] == "recognition":
        model = get_rec_model(parameters)
    else:
        model = get_gen_model(parameters)
    return model, datasets
