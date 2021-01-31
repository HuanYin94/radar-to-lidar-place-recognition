import torch
import torch.nn as nn
import torchvision
import torchvision.transforms.functional as TF
from torch.utils.data import DataLoader, Dataset

import linecache
from PIL import Image
import numpy as np

class dataLoader_train(Dataset):
    def __init__(self, tr_num, root_txt, root_radar, root_lidar, batch_size, img_H, img_W, shuffle=True):

        # from zero
        index_all = np.arange(tr_num)
        index_all = [x+1 for x in index_all]

        # shuffle
        if shuffle:
            np.random.shuffle(index_all)
        
        # split
        self.index_tr = index_all[0:tr_num]

        # params
        self.root_txt = root_txt
        self.root_radar = root_radar
        self.root_lidar = root_lidar
        self.batch_size = batch_size
        self.img_H = img_H
        self.img_W = img_W

    def read_img(self, file_name):

        img = Image.open(file_name)
        
        img_tensor = torchvision.transforms.ToTensor()(img)
        
        return img_tensor.unsqueeze(0)

    def read_txt(self, file_name):
        
        mat = np.genfromtxt(file_name, delimiter=' ')

        img_tensor = torch.from_numpy(mat)

        return img_tensor.unsqueeze(0).unsqueeze(0)

    def get_data(self, iter, device):

        print('Loading Data')

        # anchor, positive, negative
        data_anchor_radar = torch.zeros(self.batch_size, 1, self.img_H, self.img_W).to(device)
        data_anchor_lidar = torch.zeros(self.batch_size, 1, self.img_H, self.img_W).to(device)

        data_positive_radar = torch.zeros(self.batch_size, 1, self.img_H, self.img_W).to(device)
        data_positive_lidar = torch.zeros(self.batch_size, 1, self.img_H, self.img_W).to(device)

        data_negative_radar = torch.zeros(self.batch_size, 1, self.img_H, self.img_W).to(device)
        data_negative_lidar = torch.zeros(self.batch_size, 1, self.img_H, self.img_W).to(device)

        for i in range(self.batch_size):
            line_id = self.index_tr[iter*self.batch_size + i]
            line_list = linecache.getline(self.root_txt, line_id).strip()
            line_list = line_list.split()

            # from matlab: anchor_id, positive_id, negative_id 
            data_anchor_radar[i] = self.read_txt(self.root_radar+str(line_list[0])+'.txt')
            data_anchor_lidar[i] = self.read_txt(self.root_lidar+str(line_list[0])+'.txt')

            data_positive_radar[i] = self.read_txt(self.root_radar+str(line_list[1])+'.txt')
            data_positive_lidar[i] = self.read_txt(self.root_lidar+str(line_list[1])+'.txt')

            data_negative_radar[i] = self.read_txt(self.root_radar+str(line_list[2])+'.txt')
            data_negative_lidar[i] = self.read_txt(self.root_lidar+str(line_list[2])+'.txt')

        data_radar_batch = torch.cat((data_anchor_radar,data_positive_radar,data_negative_radar),0)
        data_lidar_batch = torch.cat((data_anchor_lidar,data_positive_lidar,data_negative_lidar),0)

        return data_radar_batch, data_lidar_batch