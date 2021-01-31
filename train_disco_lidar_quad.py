from torch.utils.data import Dataset, DataLoader
import torch
import torch.nn as nn
import os
import sys
import time
import numpy as np
from torch.utils.tensorboard import SummaryWriter

from loader.data_loader_train_quad import dataLoader_train
from network.lidar_coder import lidar_coder
from loss.quad_loss_fft_lidaronly import quad_loss

batch_size = 16
# SC_H = 80
# SC_W = 120
SC_H = 40
SC_W = 120

num_epoch = 10
iter_train = 512

l_rate = 0.001
decay = 0.999
w_decay = 0.001

# margin value for loss
margin_1 = 0.5
margin_2 = 0.2

# alpha 
lamda = 1

# train on part of Oxford-seq01
root_txt = '/home/yinhuan/Data/radar_lidar_pr/exp/01.12_label/train_oxford_01_quad.txt'

root_radar = '/home/yinhuan/Data/radar_lidar_pr/Oxford/seq01_80/radar_sc/'
# root_lidar = '/home/yinhuan/Data/radar_lidar_pr/Oxford/seq01_80/lidar_sc_density_raw/'
root_lidar = '/home/yinhuan/Data/radar_lidar_pr/Oxford/seq01_80/lidar_sc_occupy/'

date = '01.27_radar_lidar_pr_disco_lidar'

if __name__ == "__main__":

    device = 'cuda:2'

    if not os.path.exists('/home/yinhuan/radar_lidar_place_recognition/models/' + date):
        os.mkdir('/home/yinhuan/radar_lidar_place_recognition/models/' + date)
    if not os.path.exists('/home/yinhuan/radar_lidar_place_recognition/log/' + date):
        os.mkdir('/home/yinhuan/radar_lidar_place_recognition/log/' + date)

    print('Build Model')

    # lidar feat
    lidar_coder = lidar_coder().to(device)
    lidar_coder.train()

    # loss
    quad_loss = quad_loss(margin_1, margin_2, lamda, batch_size, SC_H, SC_W).to(device)

    writer = SummaryWriter('/home/yinhuan/radar_lidar_place_recognition/log/' + date)

    for epoch in range(num_epoch):
        print('epoch ' + str(epoch))

        # dataloader init and shuffle
        dataLoader_ = dataLoader_train(batch_size*iter_train,\
            root_txt, root_radar, root_lidar, batch_size, SC_H, SC_W, shuffle=True)

        # lr-reset for optimizer
        optimizer = torch.optim.Adam(list(lidar_coder.parameters()),\
                lr=l_rate, weight_decay=w_decay)

        for iter_ in range(iter_train):
            
            print('----------------------------------------------------' + str(iter_))
            t0 = time.time()

            radar_batch, lidar_batch = dataLoader_.get_data\
                (iter_, device)
            
            lidar_feature_batch = lidar_coder(lidar_batch)

            loss_quad, lidar_fft = quad_loss(lidar_feature_batch)

            # loss = alpha * loss_trans + loss_quad
            loss = loss_quad

            optimizer.zero_grad()

            loss.backward()

            optimizer.step()
            
            # print('%s %f %s %f'%('loss_trans:', loss_trans.data, 'loss_quad:', loss_quad.data))
            print('[%d/%d] %s %f %s %f'%(epoch, iter_, 'Loss:', loss.data, ' lr:', l_rate))
            print('time: ', time.time() - t0)

            # lr-reset for optimizer
            l_rate*=decay
            optimizer = torch.optim.Adam(list(lidar_coder.parameters()),\
                lr=l_rate, weight_decay=w_decay)

            # writer.add_scalar(date+'/Loss_translation', loss_trans, epoch*iter_train + iter_)
            # writer.add_scalar(date+'/Loss_quad', loss_quad, epoch*iter_train + iter_)

            # images = torch.cat([radar_batch[0].unsqueeze(0), radar_feature_batch[0].unsqueeze(0),\
            #      lidar_batch[0].unsqueeze(0), lidar_feature_batch[0].unsqueeze(0)])
            # writer.add_images(date+'/Images', images, iter_)
        
        # save at the last
        torch.save(lidar_coder.state_dict(), \
            '/home/yinhuan/radar_lidar_place_recognition/models/' + date + '/%s_model_%d.pth' % ('lidar_coder', epoch))

    print('Finished')
