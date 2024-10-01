from ModularHands import HandsMind
from ModularPose import PoseMinds
import os

mh = HandsMind()
mp = PoseMinds()
path = "/home/britis/Minds/Sinalizador03/Frames/Medo_frames/16MedoSinalizador03-2"
#mh.run(path)
#mp.run(path)

def is_correct(path):
    frames_num = len(os.listdir(path))
    count = 0;
    for i in os.listdir(path):
        if "_INVALIDO" in os.path.splitext(i)[0]:
            count+=1
    if count >= (frames_num/2):
        print(f"O número de frames inválidos: {count}, é muito grande, pois o arquivo possui um total de {frames_num} frames")
    else:
        print(f"O número de frames inválidos: {count}, é satisfatório, pois o arquivo possui um total de {frames_num} frames")