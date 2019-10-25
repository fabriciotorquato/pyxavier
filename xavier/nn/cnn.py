#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import math
import os

import torch

from xavier.builder.model import Model
from xavier.constants.type import Type

print("PyTorch Version: ",torch.__version__)

def cnn(filenames, name_type, show, type=Type.cnn, learning_rate=0.0004, times=3, num_epoch=25, batch_size=128, input_layer=121, output_layer=3):

    path_to_directory_models = 'models/'
    if not os.path.exists(path_to_directory_models):
        os.mkdir(path_to_directory_models)

    path_to_directory_models += name_type+'/'
    if not os.path.exists(path_to_directory_models):
        os.mkdir(path_to_directory_models)

    filenames_models= []

    for path_file in filenames:
        path = os.path.basename(os.path.dirname(path_file))
        path = path_to_directory_models+path
        path = os.path.abspath(path)
        
        filenames_models.append(path+"/")

        if not os.path.exists(path):
            os.mkdir(path)

    use_cuda = torch.cuda.is_available()
    device = torch.device("cuda:0" if use_cuda else "cpu")

    if use_cuda:
        torch.cuda.set_device(0)

    print("Algorithim use ", device)

    matriz_size = int(math.sqrt(input_layer))

    model = Model(filenames=filenames, filenames_models=filenames_models, device=device, learning_rate=learning_rate, num_epoch=num_epoch, batch_size=batch_size,
                  input_layer=input_layer, matriz_size=matriz_size, output_layer=output_layer, type=type)
    model.create_model(times=times, show=show)

    return model.file_accucary
