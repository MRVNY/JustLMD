import json 
import torch

example = json.load(open("/home/yiyu/JustLM2D/ACTOR/000000.json", 'r'))
frames = torch.load('/home/yiyu/JustLM2D/ACTOR/inf.pt')

cpt = 0

# inf.pt to a json file
json.dump({'0': frames.tolist() }, open("/home/yiyu/JustLM2D/ACTOR/inf.json", 'w'))

# for frame in frames:
#     example['annots'][0]['poses'][0] = frame.tolist()
#     #name with 000000 padding
#     json.dump(example, open("/home/yiyu/JustLM2D/ACTOR/frames/%s.json"%(str(cpt).zfill(6)), 'w'))
#     cpt += 1

