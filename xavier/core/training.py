#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import math
import time
from datetime import timedelta

import matplotlib.pyplot as plt
import numpy as np
import scikitplot as skplt
import torch
import torch.nn.functional as F
from sklearn import metrics
from torch.autograd import Variable

from xavier.constants.type import Type
from xavier.core.transformation import get_standard
from xavier.net.cnn import Cnn
from xavier.net.mlp import Mlp
from xavier.net.rnn import Rnn


class Training:

    def __init__(self, model=None, criterion=None, optimizer=None, device=None):
        self.model = model
        self.criterion = criterion
        self.optimizer = optimizer
        self.loss_tra, self.loss_val, self.feature_cnn = [], [], []
        self.device = device
        self.since = time.time()
        self.first_time = 0

    def load_model(self, type, path_model):
        self.type = type

        if self.type == Type.mlp:
            self.model = Mlp()
            checkpoint = torch.load(path_model, map_location='cpu')
            self.model.load_state_dict(checkpoint['model'])
            self.standard = checkpoint['standard']
            self.model.eval()

        elif self.type == Type.rnn:
            self.model = Rnn()
            checkpoint = torch.load(path_model, map_location='cpu')
            self.model.load_state_dict(checkpoint['model'])
            self.standard = checkpoint['standard']
            self.model.eval()

        elif self.type == Type.cnn:
            self.model = Cnn()
            checkpoint = torch.load(path_model, map_location='cpu')
            self.model.load_state_dict(checkpoint['model'])
            self.standard = checkpoint['standard']
            self.model.eval()

    def train(self, epoch, train_loader, size):
        self.since = time.time()
        self.model.train()
        test_loss = 0
        for data, target in train_loader:

            # Convert torch tensor to Variable
            data = Variable(data).to(self.device).float()
            target = Variable(target).to(self.device).long()

            # Forward + Backward + Optimize
            self.optimizer.zero_grad()  # zero the gradient buffer
            output = self.model(data).to(self.device)
            loss = self.criterion(output, target)
            loss.backward()
            self.optimizer.step()

            # Save results
            test_loss += loss.item()

        test_loss /= size
        self.loss_tra.append(test_loss)

    def validation(self, valid_loader, size, train=False):
        self.model.eval()
        test_loss = 0
        correct = 0
        with torch.no_grad():
            for data, target in valid_loader:

                # Convert torch tensor to Variable
                data = Variable(data).to(self.device).float()
                target = Variable(target).to(self.device).long()

                # Validation
                output = self.model(data).to(self.device)
                test_loss += self.criterion(output, target).item()

                _, predicted = torch.max(output, 1)
                correct += (predicted == target).sum()

        test_loss /= size
        if not train:
            self.loss_val.append(test_loss)

        time_elapsed = time.time() - self.since
        print('{}/{} [===========] - {} - loss: {:.4f} - acc: {}/{} ({:.0f}%)\n'.format(size,
                                                                                            size, timedelta(seconds=time_elapsed), test_loss, correct, size, 100. * correct / size))

    def test(self, test_loader, show, filename):
        self.model.eval()
        test_loss = 0
        correct = 0
        y_true, y_pred = [], []
        with torch.no_grad():
            for data, target in test_loader:

                # Convert torch tensor to Variable
                data = Variable(data).to(self.device).float()
                target = Variable(target).to(self.device).long()

                # Test
                output = self.model(data).to(self.device)
                test_loss += self.criterion(output, target).item()
                _, predicted = torch.max(output, 1)
                correct += (predicted == target).sum()

                if self.device != "cpu":
                    predicted = predicted.cpu().numpy()
                    target = target.cpu().numpy()

                y_pred.extend(predicted)
                y_true.extend(target)

        test_loss /= len(test_loader.dataset)

        time_elapsed = time.time() - self.first_time

        print('Test - {} -  Average loss: {:.4f} - Accuracy: {}/{} ({:.0f}%)'.format(
            timedelta(seconds=time_elapsed),
            test_loss, correct, len(test_loader.dataset),
            100. * correct / len(test_loader.dataset)))

        print('\nConfusion Matrix:')
        print(metrics.confusion_matrix(y_true, y_pred))

        test_acc = metrics.accuracy_score(y_true, y_pred)

        if show:
            plt.figure(1)
            epochs = np.arange(len(self.loss_tra))
            plt.plot(epochs, self.loss_tra, epochs, self.loss_val)
            plt.savefig('{} {:.2f}_curve.png'.format(filename, test_acc))
            skplt.metrics.plot_confusion_matrix(y_true, y_pred, normalize=True)
            # plt.show()
            plt.savefig('{} {:.2f}_matriz.png'.format(filename, test_acc))

        return np.float32(test_acc)

    def predict_mlp(self, feature):
        return np.asarray(get_standard([feature], self.standard))[0]

    def predict_cnn(self, feature):
        input_layer = 121
        matriz_size = int(math.sqrt(input_layer))
        x_row = np.asarray(
            get_standard([feature], self.standard))[0]
        arr = np.zeros(matriz_size*matriz_size - len(x_row))
        arr = np.append(x_row, arr, axis=0)
        data_standard = np.asarray(arr).reshape((matriz_size, matriz_size))
        return data_standard

    def predict_rnn(self, feature):
        input_layer = 121
        matriz_size = int(math.sqrt(input_layer))
        x_row = np.asarray(
            get_standard([feature], self.standard))[0]
        arr = np.zeros(matriz_size*matriz_size - len(x_row))
        arr = np.append(x_row, arr, axis=0)
        data_standard = np.asarray(arr).reshape((matriz_size, matriz_size))
        return data_standard

    def print_percentage(self, top_label, top_prob):
        for index in range(self.model.output_layer):
            print('option-{}: {}'.format(chr(97+top_label[0][index].item()),
                                         float(top_prob[0][index].item()) * 100))

    def predict(self, feature):
        try:
            if self.type == Type.mlp:
                data_standard = np.array([self.predict_mlp(feature)])
            elif self.type == Type.rnn:
                data_standard = np.array([self.predict_rnn(feature)])
            elif self.type == Type.cnn:
                if len(self.feature_cnn) > 2:
                    self.feature_cnn = self.feature_cnn[1:]
                    self.feature_cnn.append(self.predict_cnn(feature))
                    data_standard = np.array([self.feature_cnn])
                else:
                    self.feature_cnn.append(self.predict_cnn(feature))
                    return int(self.model.output_layer)

            self.model.zero_grad()

            data_standard = torch.LongTensor(data_standard)

            data_standard = Variable(data_standard).float()
            output = self.model(data_standard)
            top_prob, top_label = torch.topk(output, self.model.output_layer)

            self.print_percentage(top_label, top_prob)

            return str(top_label[0][0].item())
        except Exception as ex:
            print('{}'.format(ex))
