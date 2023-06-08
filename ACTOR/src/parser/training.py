import os

from .base import add_misc_options, add_cuda_options, adding_cuda, ArgumentParser
from .tools import save_args
from .dataset import add_dataset_options
from .model import add_model_options, parse_modelname
from .checkpoint import construct_checkpointname


def add_training_options(parser):
    group = parser.add_argument_group('Training options')
    group.add_argument("--batch_size", type=int, default=20, help="size of the batches")
    group.add_argument("--num_epochs", type=int, default=5000, help="number of epochs of training")
    group.add_argument("--lr", type=float, default=0.0001, help="AdamW: learning rate")
    group.add_argument("--snapshot", type=int, default=100, help="frequency of saving model/viz")
    
# python -m src.train.train_cvae --modelname cvae_transformer_rc_rcxyz_kl --pose_rep rot6d --lambda_kl 1e-5 --jointstype vertices --batch_size 20 --num_frames 60 --num_layers 8 --lr 0.0001 --glob --translation --no-vertstrans --dataset humanact12 --num_epochs 5000 --snapshot 100 --folder exps/humanact12
# python -m src.train.train_cvae --modelname cvae_transformer_rc_rcxyz_kl --glob --translation --no-vertstrans


def parser():
    parser = ArgumentParser()

    # misc options
    add_misc_options(parser)
    # --folder exps/humanact12

    # cuda options
    add_cuda_options(parser)
    
    # training options
    add_training_options(parser)
    # --batch_size 20 
    # --num_epochs 5000 
    # --snapshot 100 
    # --lr 0.0001 

    # dataset options
    add_dataset_options(parser)
    # --dataset humanact12 
    # --pose_rep rot6d 
    # --num_frames 60 
    # --glob 
    # --translation 
    # --no-vertstrans 

    # model options
    add_model_options(parser)
    # --modelname cvae_transformer_rc_rcxyz_kl 
    # --lambda_kl 1e-5 
    # --jointstype vertices 
    # --num_layers 8

    opt = parser.parse_args()
    
    # remove None params, and create a dictionnary
    parameters = {key: val for key, val in vars(opt).items() if val is not None}
    parameters['glob'] = True 
    parameters['translation'] = True
    parameters['no-vertstrans'] = False
    parameters['modelname'] = 'cvae_transformer_rc_rcxyz_kl'
    # print(parameters) # {'expname': 'exps', 'folder': 'exps/humanact12', 'cuda': True, 'batch_size': 20, 'num_epochs': 5000, 'lr': 0.0001, 'snapshot': 100, 'dataset': 'humanact12', 'num_frames': 60, 'sampling': 'conseq', 'sampling_step': 1, 'pose_rep': 'rot6d', 'max_len': -1, 'min_len': -1, 'num_seq_max': -1, 'glob': True, 'glob_rot': [3.141592653589793, 0, 0], 'translation': True, 'debug': False, 'modelname': 'cvae_transformer_rc_rcxyz_kl', 'latent_dim': 256, 'lambda_kl': 1e-05, 'lambda_rc': 1.0, 'lambda_rcxyz': 1.0, 'jointstype': 'vertices', 'vertstrans': False, 'num_layers': 8, 'activation': 'gelu'}

    # parse modelname
    ret = parse_modelname(parameters["modelname"])
    # print(ret)
    parameters["modeltype"], parameters["archiname"], parameters["losses"] = ret
    parameters['modeltype'] = 'cvae'
    parameters['archiname'] = 'transformer'
    parameters['losses'] = ['rc', 'rcxyz', 'kl']
    
    parameters["num_classes"] = 896 # * 180
    parameters["nfeats"] = 3
    parameters["njoints"] = 24
    
    # update lambdas params
    lambdas = {}
    for loss in parameters["losses"]:
        lambdas[loss] = opt.__getattribute__(f"lambda_{loss}")
    parameters["lambdas"] = lambdas
    
    if "folder" not in parameters:
        parameters["folder"] = construct_checkpointname(parameters, parameters["expname"])

    os.makedirs(parameters["folder"], exist_ok=True)
    save_args(parameters, folder=parameters["folder"])

    adding_cuda(parameters)
    
    return parameters
