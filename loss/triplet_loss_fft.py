import os
import torch
import torch.nn as nn
from torch.nn import functional as F
from loss.fft_operation import fft_operation, fftshift2d

class triplet_loss(torch.nn.Module):

    def __init__(self, margin, lamda, batch_size, SC_H, SC_W):
        super(triplet_loss, self).__init__()

        self.margin = margin
        self.lamda = lamda
        self.batch_size = batch_size
        self.SC_H = SC_H
        self.SC_W = SC_W
        self.torch_triplet_loss = nn.TripletMarginLoss(margin=self.margin, p=2, reduction='mean')
        self.pdist = nn.PairwiseDistance(p=2)

    def triplet_loss_mean(self, anchors, positives, negatives):

        loss = (self.margin + self.pdist(anchors.view(self.batch_size,-1), positives.view(self.batch_size,-1)) -\
             self.pdist(anchors.view(self.batch_size,-1), negatives.view(self.batch_size,-1)))
        
        loss = loss.clamp(min=0.0)
        loss = torch.mean(loss)
        # print(loss)
        return loss

    def forward(self, radar_feature, lidar_feature):

        radar_fft = fft_operation(radar_feature)
        lidar_fft = fft_operation(lidar_feature)

        radar_fft = fftshift2d(radar_fft)
        lidar_fft = fftshift2d(lidar_fft)

        # low filter cut
        radar_fft = radar_fft[:,:,\
                (self.SC_H//2-16):(self.SC_H//2+16), (self.SC_W//2-16):(self.SC_W//2+16)]
        lidar_fft = lidar_fft[:,:,\
                (self.SC_H//2-16):(self.SC_H//2+16), (self.SC_W//2-16):(self.SC_W//2+16)]

        fft_anchor_radar = radar_fft[0:self.batch_size-1,:,:,:].reshape(self.batch_size,-1)
        fft_anchor_lidar = lidar_fft[0:self.batch_size-1,:,:,:].reshape(self.batch_size,-1)

        fft_positive_radar = radar_fft[self.batch_size:2*self.batch_size-1,:,:,:].reshape(self.batch_size,-1)
        fft_positive_lidar = lidar_fft[self.batch_size:2*self.batch_size-1,:,:,:].reshape(self.batch_size,-1)

        fft_negative_radar = radar_fft[2*self.batch_size:3*self.batch_size-1,:,:,:].reshape(self.batch_size,-1)
        fft_negative_lidar = lidar_fft[2*self.batch_size:3*self.batch_size-1,:,:,:].reshape(self.batch_size,-1)

        # 2*2*2 cases
        L1 = self.triplet_loss_mean(fft_anchor_radar, fft_positive_radar, fft_negative_radar)
        L2 = self.triplet_loss_mean(fft_anchor_radar, fft_positive_radar, fft_negative_lidar)
        L3 = self.triplet_loss_mean(fft_anchor_radar, fft_positive_lidar, fft_negative_radar)
        L4 = self.triplet_loss_mean(fft_anchor_radar, fft_positive_lidar, fft_negative_lidar)

        L5 = self.triplet_loss_mean(fft_anchor_lidar, fft_positive_radar, fft_negative_radar)
        L6 = self.triplet_loss_mean(fft_anchor_lidar, fft_positive_radar, fft_negative_lidar)
        L7 = self.triplet_loss_mean(fft_anchor_lidar, fft_positive_lidar, fft_negative_radar)
        L8 = self.triplet_loss_mean(fft_anchor_lidar, fft_positive_lidar, fft_negative_lidar)

        print('[%s %f], [%s %f], [%s %f], [%s %f], [%s %f], [%s %f], [%s %f], [%s %f]'%\
            ('rrr', L1.detach().cpu().numpy(), 'rrl', L2.detach().cpu().numpy(), 'rlr', L3.detach().cpu().numpy(),\
                 'rll', L4.detach().cpu().numpy(), 'lrr',L5.detach().cpu().numpy(), 'lrl', L6.detach().cpu().numpy(),\
                      'llr', L7.detach().cpu().numpy(), 'lll', L8.detach().cpu().numpy()))

        loss = L1 + L2 + self.lamda*(L3 + L4 + L5 + L6) + L7 + L8

        return loss, radar_fft, lidar_fft