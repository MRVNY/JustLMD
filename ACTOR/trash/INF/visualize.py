from nosmpl.smpl_onnx import SMPLOnnxRuntime
from nosmpl.vis.vis_o3d import Open3DVisualizer

import os
import torch
import numpy as np

# smpl = SMPLOnnxRuntime()

# poses = torch.load('ATS.pt')

# o3d_vis = Open3DVisualizer(fps=30, save_img_folder='./ATS', enable_axis=False)

# poses = poses.reshape(180,24,3)
# poses = torch.index_select(poses, dim=1, index=torch.arange(0, poses.size(1)-1))
# poses = poses.detach().numpy()

# global_orient = [[[0,0,0]]]
# # global_orient = np.random.randn(1, 1, 3).astype(np.float32)
# trans = [0,0,0]

# for body in poses:
#     data = smpl.forward(body[None], global_orient)

#     [vertices, joints, faces] = data
#     vertices = vertices[0].squeeze()
#     joints = joints[0].squeeze()
#     faces = faces.astype(np.int32)

#     o3d_vis.update(vertices, faces, trans, R_along_axis=[0, 0, 0], waitKey=1)

# o3d_vis.release()

lyrics = 'Cause maybe the night that my dreams might let me know  All the stars are closer, all the stars are closer all the stars are closer'

# os.system('ffmpeg -framerate 30 -i ATS/temp_%04d.png -c:v libx264 -r 30 -pix_fmt yuv420p ATS/output.mp4')
# os.system('rm ATS/*.png')
# os.system('ffmpeg -i /Users/Marvin/NII_Code/JustLM2D/Songs_Test/AllTheStarsbyKendrickLamarftSZAJustDance2021/audio.wav\
#     -ss "00:46.530" -t 00:06 -c copy ATS/output.wav')
# os.system('ffmpeg -i ATS/output.mp4 -i ATS/output.wav -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 ATS/video.mp4')
os.system("ffmpeg -i ATS/video.mp4 -vf \"drawtext=fontfile=Roboto-Regular.ttf:text='%s':fontsize=30:x=(w-tw)/2:y=h-th-10:fontcolor=black\" -codec:a copy ATS/ATS.mp4"%lyrics)