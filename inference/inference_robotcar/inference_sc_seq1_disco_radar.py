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
from network.radar2lidar_relu import radar_transformer
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

total_num = 8866  # RobotCar seq01
# total_num = 3298 # KAIST01
# total_num = 3586 # KAIST02
# total_num = 2212 # DCC01
# total_num = 3025 # DCC02

start_id = 7599
end_id = 8300

# Data

root_radar_path = '/home/yinhuan/Data/radar_lidar_pr/Oxford/seq01_80/radar_sc/'
root_lidar_path = '/home/yinhuan/Data/radar_lidar_pr/Oxford/seq01_80/lidar_sc_occupy/'
# save_radar_fft_path = '/home/yinhuan/Data/radar_lidar_pr/Oxford/seq01_80/radar_fft_disco_rr/'
save_radar_fft_path = '/home/yinhuan/Data/radar_lidar_pr/Oxford/seq01_80/radar_fft_disco_rr_quad/'

# model
# radar_coder_path = '/home/yinhuan/radar_lidar_place_recognition/models/01.18_radar_lidar_pr_disco_radar/radar_coder_model_9.pth'
radar_coder_path = '/home/yinhuan/radar_lidar_place_recognition/models/01.27_radar_lidar_pr_disco_radar/radar_coder_model_5.pth'

if __name__ == "__main__":

    device = 'cuda:3'

    np.set_printoptions(precision=5)

    print('Build Model')

    # radar coder init 
    radar_coder = radar_coder().to(device)
    radar_coder.load_state_dict(torch.load(radar_coder_path))
    radar_coder.eval()
    for m in radar_coder.modules():
        if isinstance(m, nn.BatchNorm2d):
            m.track_running_stats=False

    # dataloader init and shuffle
    dataLoader_ = dataLoader_inference(total_num, root_radar_path, root_lidar_path, SC_H, SC_W)

    pdist = nn.PairwiseDistance(p=2)

    # count the num 
    for iter_ in range(start_id, end_id):
            
            print('----------------------------------------------------' + str(iter_))
            t0 = time.time()

            radar_data, lidar_data = dataLoader_.get_data\
                (iter_+1, device) # from 1, not 0

            # radar_translated = radar_transformer(radar_data)
            # use both lidar_coder ?

            radar_feature = radar_coder(radar_data)

            radar_fft = fft_operation(radar_feature)
            
            radar_fft = fftshift2d(radar_fft)

            radar_fft = radar_fft[:,:,\
                 (SC_H//2-16):(SC_H//2+16), (SC_W//2-16):(SC_W//2+16)]

            # save txt
            if not os.path.exists(save_radar_fft_path):
                os.makedirs(save_radar_fft_path)

            radar_fft_np = radar_fft.view(32, 32).detach().cpu().numpy()
            with open(save_radar_fft_path + str(iter_+1) + '.txt', 'wb') as f:
                np.savetxt(f, radar_fft_np, fmt='%5.5f', delimiter=' ', newline='\n')

            # images = torch.cat([radar_batch[0].unsqueeze(0), radar_feature_batch[0].unsqueeze(0),\
            #      lidar_batch[0].unsqueeze(0), lidar_feature_batch[0].unsqueeze(0)])
            # writer.add_images(date+'/Images', images, iter_)

    print('Finished')
