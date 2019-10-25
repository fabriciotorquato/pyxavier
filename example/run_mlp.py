#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import sys
from glob import glob
import torch
from xavier.nn.mlp import mlp
from argparse import ArgumentParser


def get_args():
    parser = ArgumentParser(description='Xavier')
    parser.add_argument('--show', '-s', action='store_true')
    parser.add_argument('--full', '-f', action='store_false')
    parser.add_argument('--dir', '-d', type=str, default='bci')
    args = parser.parse_args()
    return args


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

    result = mlp(filenames=filenames, name_type=name_type,
                 show=show, times=1, output_layer=3)

    print("MLP:")
    print("->", result, "\n")
