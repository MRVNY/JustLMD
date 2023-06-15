'''
Demo code to run NoSMPL visualize
'''
from nosmpl.smpl_onnx import SMPLOnnxRuntime
import numpy as np
import open3d as o3d

import torch

import collections
import onnxruntime as rt
import torch
import numpy as np
from nosmpl.vis.vis_o3d import vis_mesh_o3d, Open3DVisualizer
import json
from alfred import print_shape
from nosmpl.utils import rot_mat_to_euler, rotmat_to_rotvec
import sys

smpl = SMPLOnnxRuntime()

poses = torch.load('ATS.pt')

o3d_vis = Open3DVisualizer(fps=30, enable_axis=False)

poses = poses.reshape(180,24,3)
poses = torch.index_select(poses, dim=1, index=torch.arange(0, poses.size(1)-1))
poses = poses.detach().numpy()

global_orient = [[[0,0,0]]]
# global_orient = np.random.randn(1, 1, 3).astype(np.float32)
trans = [0,0,0]

for body in poses:
    data = smpl.forward(body[None], global_orient)

    [vertices, joints, faces] = data
    vertices = vertices[0].squeeze()
    joints = joints[0].squeeze()

    faces = faces.astype(np.int32)
    # vis_mesh_o3d(vertices, faces)
    # vertices += trans
    # trans = [trans[1], trans[0], trans[2]]
    # trans = [trans[0], trans[1], 0]
    o3d_vis.update(vertices, faces, trans, R_along_axis=[0, 0, 0], waitKey=1)
    
o3d_vis.release()
