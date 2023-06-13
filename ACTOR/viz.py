import json 
import torch

example = json.load(open("/Users/Marvin/NII_Code/JustLM2D/Baseline/000000.json", 'r'))
# frames = torch.load('/Users/Marvin/NII_Code/JustLM2D/ACTOR/inf.pt')
frames = json.load(open("/Users/Marvin/NII_Code/JustLM2D/ACTOR/inf.json", 'r'))['0']

cpt = 0

for frame in frames:
    example['annots'][0]['poses'][0] = frame
    #name with 000000 padding
    json.dump(example, open("/Users/Marvin/NII_Code/JustLM2D/ACTOR/frames/%s.json"%(str(cpt).zfill(6)), 'w'))
    cpt += 1
