import torch
import torch.nn as nn
import torchvision
import torchvision.transforms.functional as TF
from torch.utils.data import DataLoader, Dataset

import linecache
from PIL import Image
import numpy as np

class dataLoader_inference(Dataset):
    def __init__(self, test_num, root_radar, root_lidar, img_H, img_W):

        # from zero
        index_all = np.arange(test_num)
        index_all = [x+1 for x in index_all]
        
        # split
        self.index_tr = index_all[0:test_num]

        # params
        self.root_radar = root_radar
        self.root_lidar = root_lidar
        self.img_H = img_H
        self.img_W = img_W

    def read_img(self, file_name):

        img = Image.open(file_name)
        
        img_tensor = torchvision.transforms.ToTensor()(img)
        
        return img_tensor.unsqueeze(0)

    def read_txt(self, file_name):

        mat = np.loadtxt(file_name, delimiter=' ')
        
        img_tensor = torch.from_numpy(mat)
        
        return img_tensor.unsqueeze(0).unsqueeze(0)

    def get_data(self, iter, device):

        print('Loading Data')

        # one lidar and one radar
        data_radar = torch.zeros(1, 1, self.img_H, self.img_W).to(device)
        data_lidar = torch.zeros(1, 1, self.img_H, self.img_W).to(device)

        data_radar[0] = self.read_txt(self.root_radar+str(iter)+'.txt')
        data_lidar[0] = self.read_txt(self.root_lidar+str(iter)+'.txt')

        return data_radar, data_lidar