from torch.utils.data import Dataset, DataLoader
import torch
import torch.nn as nn
import os
import sys
import time
import numpy as np
from torch.utils.tensorboard import SummaryWriter

sys.path.append("..")

from loader.data_loader_inference import dataLoader_inference
from network.radar_coder import radar_coder
from network.lidar_coder import lidar_coder
from loss.fft_operation import fft_operation, fftshift2d

import torchvision
import torchvision.transforms.functional as TF
from PIL import Image
import copy

# 2020.12.24
SC_H = 40
SC_W = 120
# SC_H = 64
# SC_W = 120

# total_num = 8866  # RobotCar
# total_num = 3298 # KAIST01
# total_num = 3586 # KAIST02
# total_num = 2212 # DCC01
# total_num = 3025 # DCC02
# total_num = 2214
total_num = 3252

# Data
root_radar_path = '/home/yinhuan/Data/radar_lidar_pr/Mulran/Riverside02_80/radar_sc/'
# root_lidar_path = '/home/yinhuan/Data/radar_lidar_pr/Mulran/Riverside02_80/lidar_sc_density/'
root_lidar_path = '/home/yinhuan/Data/radar_lidar_pr/Mulran/Riverside02_80/lidar_sc_occupy/'
save_lidar_fft_path = '/home/yinhuan/Data/radar_lidar_pr/Mulran/Riverside02_80/lidar_fft_disco_ll_quad/'

# model
lidar_coder_path = '/home/yinhuan/radar_lidar_place_recognition/models/01.27_radar_lidar_pr_disco_lidar/lidar_coder_model_5.pth'

if __name__ == "__main__":

    device = 'cuda:3'

    np.set_printoptions(precision=5)

    print('Build Model')

    # lidar coder init
    lidar_coder = lidar_coder().to(device)
    lidar_coder.load_state_dict(torch.load(lidar_coder_path))
    lidar_coder.eval()
    for m in lidar_coder.modules():
        if isinstance(m, nn.BatchNorm2d):
            m.track_running_stats=False

    # dataloader init and shuffle
    dataLoader_ = dataLoader_inference(total_num, root_radar_path, root_lidar_path, SC_H, SC_W)

    pdist = nn.PairwiseDistance(p=2)

    # count the num 
    for iter_ in range(total_num):
            
            print('----------------------------------------------------' + str(iter_))
            t0 = time.time()

            radar_data, lidar_data = dataLoader_.get_data\
                (iter_+1, device) # from 1, not 0


            lidar_feature = lidar_coder(radar_data)

            lidar_fft = fft_operation(lidar_feature)
            
            lidar_fft = fftshift2d(lidar_fft)

            lidar_fft = lidar_fft[:,:,\
                 (SC_H//2-16):(SC_H//2+16), (SC_W//2-16):(SC_W//2+16)]

            # save txt
            if not os.path.exists(save_lidar_fft_path):
                os.makedirs(save_lidar_fft_path)

            lidar_fft_np = lidar_fft.view(32, 32).detach().cpu().numpy()
            with open(save_lidar_fft_path + str(iter_+1) + '.txt', 'wb') as f:
                np.savetxt(f, lidar_fft_np, fmt='%5.5f', delimiter=' ', newline='\n')

            # images = torch.cat([radar_batch[0].unsqueeze(0), radar_feature_batch[0].unsqueeze(0),\
            #      lidar_batch[0].unsqueeze(0), lidar_feature_batch[0].unsqueeze(0)])
            # writer.add_images(date+'/Images', images, iter_)

    print('Finished')
