import torch
import torch.nn as nn
import torch.nn.functional as F


class Cnn(nn.Module):
    def __init__(self, device=None):
        super(Cnn, self).__init__()
        self.device = device
        self.output_layer = 3
        self.conv0 = nn.Sequential(
            nn.Conv2d(3, 8, 4, 1, 1).to(self.device),
            nn.BatchNorm2d(8, False).to(self.device)
        )
        self.conv2 = nn.Sequential(
            nn.Conv2d(8, 16, 4, 1, 1).to(self.device),
            nn.BatchNorm2d(16, False).to(self.device),
            nn.MaxPool2d(2).to(self.device)
        )
        self.dense = nn.Sequential(
            nn.Linear(8 * 8 * 4, 32).to(self.device),
            nn.Tanh().to(self.device),
            nn.Linear(32, 32).to(self.device),
            nn.Tanh().to(self.device),
            nn.Linear(32, self.output_layer).to(self.device),
        )

    def forward(self, x):
        x = self.conv0(x).to(self.device)
        x = self.conv2(x).to(self.device)
        x = x.view(x.size(0), -1)
        x = self.dense(x).to(self.device)
        return torch.softmax(x, dim=1).to(self.device)
