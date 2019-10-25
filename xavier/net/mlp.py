import torch
import torch.nn.functional as F
from torch import nn


class Mlp(nn.Module):
    def __init__(self, device=None):
        super(Mlp, self).__init__()
        self.device = device
        self.output_layer = 3
        self.dense = nn.Sequential(
            nn.Linear(112, 32).to(self.device),
            nn.Tanh().to(self.device),
            nn.Linear(32, 32).to(self.device),
            nn.Tanh().to(self.device),
            nn.Linear(32, self.output_layer).to(self.device),
        )

    def forward(self, x):
        x = self.dense(x).to(self.device)
        return torch.softmax(x, dim=1).to(self.device)
