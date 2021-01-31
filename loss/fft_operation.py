import os
import torch
import torch.nn as nn
from torch.nn import functional as F

def fft_operation(batch_data):
    
    median_output = torch.rfft(batch_data, 2, normalized=True, onesided=False)
    median_output_r = median_output[:, :, :, :, 0]
    median_output_i = median_output[:, :, :, :, 1]
    output = torch.sqrt(median_output_r ** 2 + median_output_i ** 2 + 1e-15)

    return output

def fftshift2d(x):
    for dim in range(1, len(x.size())):
        n_shift = x.size(dim)//2
        if x.size(dim) % 2 != 0:
            n_shift = n_shift + 1  # for odd-sized images
        x = roll_n(x, axis=dim, n=n_shift)
    return x  # last dim=2 (real&imag)

def roll_n(X, axis, n):
    f_idx = tuple(slice(None, None, None) if i != axis else slice(0, n, None) for i in range(X.dim()))
    b_idx = tuple(slice(None, None, None) if i != axis else slice(n, None, None) for i in range(X.dim()))
    front = X[f_idx]
    back = X[b_idx]
    return torch.cat([back, front], axis)