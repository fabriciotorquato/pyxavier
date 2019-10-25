#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from glob import glob
from argparse import ArgumentParser
from xavier.builder.dataset import Dataset


def get_args():
    parser = ArgumentParser(description='Xavier')
    parser.add_argument('--dir', type=str, default='bci')
    parser.add_argument('--full', type=bool, default=True)
    args = parser.parse_args()
    return args


if __name__ == "__main__":

    args = get_args()

    name_type = args.dir
    full = args.full

    path_to_directory = 'dataset/{}/'.format(name_type)
    filenames = glob(os.path.join(path_to_directory, "*", ""))
    dataset = None

    for idx, file in enumerate(filenames):
        if file.rpartition('/')[0].rpartition('/')[2] != 'full':
            values = '{}values.csv'.format(file)
            random = '{}data_random.txt'.format(file)
            classification = '{}classification.txt'.format(file)
            dataList = '{}dataList.csv'.format(file)
            dataset = Dataset(values, classification, random, dataList, file)

    if dataset is not None and full:
        dataset.merge_files(path_to_directory + 'full/', filenames)
