#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import sys
from glob import glob
from argparse import ArgumentParser

from xavier.nn.mlp import mlp
from xavier.nn.rnn import rnn
from xavier.nn.cnn import cnn


def get_args():
    parser = ArgumentParser(description='Xavier')
    parser.add_argument('--show', '-s', action='store_true')
    parser.add_argument('--full', '-f', action='store_false')
    parser.add_argument('--dir', '-d', type=str, default='bci')
    args = parser.parse_args()
    return args


def start_train(filenames, name_type, show):
    results = []

    results.append(mlp(filenames=filenames, name_type=name_type,
                       show=show, times=1,  output_layer=3))
    results.append(rnn(filenames=filenames, name_type=name_type,
                       show=show, times=1,  output_layer=3))
    results.append(cnn(filenames=filenames, name_type=name_type,
                       show=show, times=1,  output_layer=3))

    for idx, result in enumerate(results):
        if idx == 0:
            print("MLP:")
        elif idx == 1:
            print("RNN:")
        elif idx == 2:
            print("CNN")
        print("->", result, "")


if __name__ == "__main__":

    args = get_args()

    name_type = args.dir
    show = args.show
    full = args.full

    path_to_directory = 'dataset/'+name_type+'/'
    if full:
        filenames = [path_to_directory+"full/"]
    else:
        filenames = glob(os.path.join(path_to_directory, "*", ""))

    start_train(filenames, name_type, show)
