import os
import torch
import torch.nn as nn
from torch.nn import functional as F
from loss.fft_operation import fft_operation, fftshift2d

class quad_loss(torch.nn.Module):
    def __init__(self, margin_1, margin_2, lamda, batch_size, SC_H, SC_W):
        super(quad_loss, self).__init__()

        self.margin_1 = margin_1
        self.margin_2 = margin_2

        self.lamda = lamda
        self.batch_size = batch_size

        self.SC_H = SC_H
        self.SC_W = SC_W
        
        self.pdist = nn.PairwiseDistance(p=2)

    def quad_loss_mean(self, anchors, positives, negatives_1, negatives_2):

        loss_1 = (self.margin_1 + self.pdist(anchors.view(self.batch_size,-1), positives.view(self.batch_size,-1)) -\
             self.pdist(anchors.view(self.batch_size,-1), negatives_1.view(self.batch_size,-1)))

        loss_2 = (self.margin_2 + self.pdist(anchors.view(self.batch_size,-1), positives.view(self.batch_size,-1)) -\
             self.pdist(negatives_1.view(self.batch_size,-1), negatives_2.view(self.batch_size,-1)))
        
        loss = loss_1 + loss_2
        loss = loss.clamp(min=0.0)
        loss = torch.mean(loss)
        # print(loss)
        return loss

    def forward(self, lidar_feature):

        lidar_fft = fft_operation(lidar_feature)

        lidar_fft = fftshift2d(lidar_fft)

        # cut
        lidar_fft = lidar_fft[:,:,\
                (self.SC_H//2-16):(self.SC_H//2+16), (self.SC_W//2-16):(self.SC_W//2+16)]

        fft_anchor_lidar = lidar_fft[0:self.batch_size-1,:,:,:].reshape(self.batch_size,-1)

        fft_positive_lidar = lidar_fft[self.batch_size:2*self.batch_size-1,:,:,:].reshape(self.batch_size,-1)

        fft_negative_1_lidar = lidar_fft[2*self.batch_size:3*self.batch_size-1,:,:,:].reshape(self.batch_size,-1)

        fft_negative_2_lidar = lidar_fft[3*self.batch_size:4*self.batch_size-1,:,:,:].reshape(self.batch_size,-1)

        # radar PR
        # L1 = self.quad_loss_mean(fft_anchor_radar, fft_positive_radar, fft_negative_1_radar, fft_negative_2_radar)

        # # lidar PR
        L2 = self.quad_loss_mean(fft_anchor_lidar, fft_positive_lidar, fft_negative_1_lidar, fft_negative_2_lidar)

        # # radar-lidar PR
        # L3 = self.quad_loss_mean(fft_anchor_radar, fft_positive_lidar, fft_negative_1_radar, fft_negative_2_lidar)
        # L4 = self.quad_loss_mean(fft_anchor_radar, fft_positive_lidar, fft_negative_1_lidar, fft_negative_2_radar)
        # L5 = self.quad_loss_mean(fft_anchor_lidar, fft_positive_radar, fft_negative_1_radar, fft_negative_2_lidar)
        # L6 = self.quad_loss_mean(fft_anchor_lidar, fft_positive_radar, fft_negative_1_lidar, fft_negative_2_radar)


        # print('[%s %f], [%s %f], [%s %f], [%s %f], [%s %f], [%s %f]'%\
        #     ('rrrr', L1.detach().cpu().numpy(), 'llll', L2.detach().cpu().numpy(), 'rlrl', L3.detach().cpu().numpy(),\
        #          'rllr', L4.detach().cpu().numpy(), 'lrrl',L5.detach().cpu().numpy(), 'lrlr', L6.detach().cpu().numpy()))

        # loss = L1 + L2 + self.lamda*(L3 + L4 + L5 + L6)

        loss = L2

        return loss, lidar_fft