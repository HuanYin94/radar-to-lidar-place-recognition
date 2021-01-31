import os
import torch
import torch.nn as nn

class doubleNet(nn.Module):
    def __init__(self, i_channel, o_channel, m_channel=None):
        super(doubleNet, self).__init__()

        if not m_channel:
            m_channel = o_channel

        self.net = nn.Sequential(
        nn.Conv2d(i_channel, m_channel, kernel_size=3, padding=1),
        nn.BatchNorm2d(m_channel),
        nn.ReLU(inplace=True),
        nn.Conv2d(m_channel, o_channel, kernel_size=3, padding=1),
        nn.BatchNorm2d(o_channel),
        nn.ReLU(inplace=True))

    def forward(self, input):
        return self.net(input)

class singleNet(nn.Module):
    def __init__(self, i_channel, o_channel):
        super(singleNet, self).__init__()

        self.net = nn.Sequential(
        nn.Conv2d(i_channel, o_channel, kernel_size=3, padding=1),
        nn.BatchNorm2d(o_channel),
        nn.ReLU(inplace=True))

    def forward(self, input):
        return self.net(input)

class unet(nn.Module):
    def __init__(self, i_channel, o_channel):
        super(unet, self).__init__()

        self.pool = nn.MaxPool2d(2)

        self.conv_down_1 = doubleNet(i_channel, 64)
        self.conv_down_2 = doubleNet(64, 128)
        self.conv_down_3 = doubleNet(128, 256)
        self.conv_down_4 = doubleNet(256, 256)

        self.tr_up_4 = nn.Upsample(scale_factor=2, mode='nearest')
        self.tr_up_3 = nn.Upsample(scale_factor=2, mode='nearest')
        self.tr_up_2 = nn.Upsample(scale_factor=2, mode='nearest')

        self.conv_up_4 = doubleNet(512, 128, 256)
        self.conv_up_3 = doubleNet(256, 64, 128) 
        self.conv_up_2 = doubleNet(128, o_channel, 64)

    def forward(self, i):

        # down
        f_down_1 = self.conv_down_1(i)
        f_down_1p = self.pool(f_down_1)

        f_down_2 = self.conv_down_2(f_down_1p)
        f_down_2p = self.pool(f_down_2)

        f_down_3 = self.conv_down_3(f_down_2p)
        f_down_3p = self.pool(f_down_3)

        f_down_4 = self.conv_down_4(f_down_3p)

        # up
        f_up_4t = self.tr_up_4(f_down_4)
        f_merge_4 = torch.cat([f_down_3, f_up_4t], dim=1)
        f_up_4 = self.conv_up_4(f_merge_4)

        f_up_3t = self.tr_up_3(f_up_4)
        f_merge_3 = torch.cat([f_down_2, f_up_3t], dim=1)
        f_up_3 = self.conv_up_3(f_merge_3)

        f_up_2t = self.tr_up_2(f_up_3)
        f_merge_2 = torch.cat([f_down_1, f_up_2t], dim=1)
        f_up_2 = self.conv_up_2(f_merge_2)

        return f_up_2

class radar_coder(nn.Module):
    def __init__(self):
        super(radar_coder, self).__init__()

        self.radar_nn = unet(1,64)
        self.feat_net_radar = nn.Conv2d(64, 1, kernel_size=1)

    def forward(self, radar_sc_batch):

        # feature for both scan & map
        radar_batch_feature = self.feat_net_radar(self.radar_nn(radar_sc_batch))

        return radar_batch_feature