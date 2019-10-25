import torch
import torch.nn.functional as F
from torch import nn


class Rnn(nn.Module):
    def __init__(self, device=None):
        super(Rnn, self).__init__()
        self.input_size = 11
        self.hidden_lstm_size = 16
        self.hidden_size = 8
        self.num_layers = 1
        self.output_layer = 3
        self.device = device

        self.lstm_layer_1 = nn.LSTM(self.input_size, self.hidden_lstm_size,self.num_layers, batch_first=True).to(self.device)

        self.dropout = nn.Dropout2d(p=0.2).to(self.device)

        self.lstm_layer_2 = nn.LSTM(self.hidden_lstm_size, self.hidden_lstm_size,self.num_layers, batch_first=True).to(self.device)

        self.dense = nn.Sequential(
            nn.Linear(self.hidden_lstm_size, self.hidden_size).to(self.device),
            nn.Linear(self.hidden_size, self.hidden_size).to(self.device),
            nn.Linear(self.hidden_size, self.output_layer).to(self.device),
        )

    def forward(self, x):

        # Forward propagate LSTM
        # out: tensor of shape (batch_size, seq_length, hidden_size)
        x, _ = self.lstm_layer_1(x)

        # x = torch.relu(x).to(self.device)

        x = self.dropout(x).to(self.device)

        x, _ = self.lstm_layer_2(x)

        x = torch.softmax(x, dim=1).to(self.device)

        x = x[:, -1, :]

        x = self.dense(x).to(self.device)

        return torch.softmax(x, dim=1).to(self.device)
