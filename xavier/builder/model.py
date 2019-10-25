#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time

import numpy as np
import torch
import torch.optim as optim
from sklearn.model_selection import train_test_split
from torch import nn

import xavier.constants.config as config
from xavier.constants.type import Type
from xavier.core.dataLoader import DataLoader
from xavier.core.dataset import Dataset
from xavier.core.training import Training
from xavier.core.transformation import get_standard, init_standard
from xavier.net.cnn import Cnn
from xavier.net.mlp import Mlp
from xavier.net.rnn_lstm_2 import Rnn

torch.manual_seed(1234)


class Model(object):

    def __init__(self, filenames, filenames_models, device, learning_rate, num_epoch, batch_size, input_layer=0, hidden_layer=0, output_layer=3, matriz_size=0, type=Type.mlp):

        self.input_layer = input_layer
        self.hidden_layer = hidden_layer
        self.output_layer = output_layer
        self.matriz_size = matriz_size
        self.device = device
        self.filenames = filenames
        self.matriz_size = matriz_size
        self.type = type
        self.batch_size = batch_size
        self.learning_rate = learning_rate
        self.filenames_models = filenames_models
        self.num_epoch = num_epoch
        self.file_accucary = np.zeros(len(self.filenames))
        self.version = config.VERSION

    def __train_model(self, train_loader, valid_loader, test_loader, train_size, valid_size, show, filename):
        self.model.first_time = time.time()
        for epoch in range(1, self.num_epoch+1):
            print "Epoch " + str(epoch) + "/" + str(self.num_epoch)
            self.model.train(epoch, train_loader, train_size)    
            self.model.validation(valid_loader, valid_size)
        print('Data train: ')
        self.model.validation(train_loader, train_size, train=True)
        print('Data Test: ')
        return self.model.test(test_loader, show, filename)

    def __build_model(self):
        # build Model
        if self.type == Type.mlp:
            model = Mlp(self.device).to(self.device)
        elif self.type == Type.rnn:
            model = Rnn(self.device).to(self.device)
            print(model)
        elif self.type == Type.cnn:
            model = Cnn(self.device).to(self.device)

        # choose optimizer and loss function
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(model.parameters(), lr=self.learning_rate)

        model = model.to(self.device)

        model_training = Training(
            model, criterion, optimizer, self.device)

        return model_training

    def get_dataset(self, file):
        dataset = np.loadtxt(file + 'dataset.csv',
                                    delimiter=',', dtype=np.float64)
        dataset_x = np.asarray([l[1:] for l in dataset])
        dataset_y = np.asarray([l[0] for l in dataset])

        return dataset_x, dataset_y

    def get_normalization(self, X_train, X_test):
        if self.type == Type.mlp:
            X_train, standard = init_standard(X_train)
            X_test = get_standard(X_test, standard)
            return X_train, X_test, standard
        elif self.type == Type.rnn:
            X_train, standard = init_standard(X_train)
            X_test = get_standard(X_test, standard)
            return X_train, X_test, standard
        elif self.type == Type.cnn:
            X_train, standard = init_standard(X_train)
            X_test = get_standard(X_test, standard)
            return X_train, X_test, standard

    def get_loader(self, type, batch_size, X_train, y_train, X_test, y_test, matriz_size):

        if type == Type.mlp:
            train_data = Dataset(X_train, y_train, Type.mlp)
            test_data = Dataset(X_test, y_test, Type.mlp)
        elif type == Type.rnn:
            train_data = Dataset(X_train, y_train,  Type.rnn, matriz_size)
            test_data = Dataset(X_test, y_test,  Type.rnn, matriz_size)
        elif type == Type.cnn:
            train_data = Dataset(X_train, y_train, Type.cnn, matriz_size)
            test_data = Dataset(X_test, y_test, Type.cnn, matriz_size)

        dataLoader = DataLoader()
        train_loader, valid_loader, train_size, valid_size = dataLoader.get_train(
            train_data, batch_size)

        test_loader = dataLoader.get_test(test_data, batch_size)

        return train_loader, valid_loader, test_loader, train_size, valid_size

    def save_model(self, type, path_model, model, acc, standard):
        # Save the Trained Model
        path = path_model+type.value
        if not os.path.exists(path):
            os.mkdir(path)

        filename = path + '/'+self.version+' {:.2f}'.format(acc)+'.pkl'

        torch.save({
            'model': model.model.state_dict(),
            'standard': standard
        }, filename)

    def create_model(self, times, show):
        self.file_accucary = np.zeros(len(self.filenames))
        for _ in range(times):
            for idx, file in enumerate(self.filenames):
                print "\nTraining dataset: " + str(file) + "\n"

                dataset_x, dataset_y = self.get_dataset(file)

                X_train, X_test, y_train, y_test = train_test_split(
                    dataset_x, dataset_y, test_size=0.2, random_state=21)

                X_train, X_test, standard = self.get_normalization(
                    X_train, X_test)

                train_loader, valid_loader, test_loader, train_size, valid_size = self.get_loader(
                    self.type, self.batch_size, X_train, y_train, X_test, y_test, self.matriz_size)

                self.input_layer = X_train.shape[1]
                self.model = self.__build_model()

                path = self.filenames_models[idx] + \
                    self.type.value + '/'+self.version

                accuracy = self.__train_model(train_loader, valid_loader,
                                              test_loader, train_size, valid_size, show, filename=path)

                if accuracy > self.file_accucary[idx]:
                    self.save_model(self.type,
                                    self.filenames_models[idx], self.model, accuracy, standard)
                    self.file_accucary[idx] = accuracy
