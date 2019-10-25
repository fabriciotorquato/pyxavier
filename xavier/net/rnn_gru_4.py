import torch
import torch.nn.functional as F
from torch import nn


class Rnn(nn.Module):
    def __init__(self, device=None):
        super(Rnn, self).__init__()
        self.input_size = 11
        self.hidden_size = 16
        self.num_layers = 4
        self.output_layer = 3
        self.device = device
        self.lstm = nn.GRU(self.input_size, self.hidden_size,
                           self.num_layers, batch_first=True).to(self.device)
        self.fc = nn.Linear(
            self.hidden_size, self.output_layer).to(self.device)

    def forward(self, x):

        # Forward propagate LSTM
        # out: tensor of shape (batch_size, seq_length, hidden_size)
        x, _ = self.lstm(x)

        # Decode the hidden state of the last time step
        x = self.fc(x[:, -1, :]).to(self.device)
        return torch.softmax(x, dim=1).to(self.device)
