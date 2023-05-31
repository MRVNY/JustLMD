import os 

for dir in os.listdir('/home/yiyu/Downloads/Songs'):
    if os.path.exists('/home/yiyu/Downloads/Songs/%s/video.mp4'%dir):
        os.remove('/home/yiyu/Downloads/Songs/%s/video.mp4'%dir)
    if os.path.exists('/home/yiyu/Downloads/Songs/%s/audio.wav'%dir):
        os.remove('/home/yiyu/Downloads/Songs/%s/audio.wav'%dir)