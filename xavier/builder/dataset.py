#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import os

import numpy as np
import pandas
from scipy import stats
from tqdm import tqdm

from xavier.core.classification import Classification
from xavier.core.transformation import get_feature, get_frequency


class Dataset(object):

    def __init__(self, file_csv, classification, randomList, imageList, saveFolder):

        self.file_csv = file_csv
        self.classification = classification
        self.randomList = randomList
        self.imageList = imageList
        self.saveFolder = saveFolder

        self.classification = Classification(
            self.file_csv,  self.classification, self.saveFolder)

        self._create_dataset()

    def _get_labels(self, randomList, imageList, seconds):
        file_csv = open(randomList)

        data_csv_randomList = csv.reader(file_csv)
        data_csv_randomList = np.array(
            [np.array(row) for row in data_csv_randomList])

        file_csv = open(imageList)

        data_csv_imageList = csv.reader(file_csv)
        data_csv_imageList = np.array(
            [np.array(row) for row in data_csv_imageList])
        data_csv_imageList = data_csv_imageList.T
        labels = []

        for row in data_csv_randomList:
            value = row[0].split(" ", 1)[1]
            index = data_csv_imageList[1].tolist().index(value)
            for _ in range(seconds):
                labels.append(data_csv_imageList[0][index])

        return labels

    def _create_dataset(self):
        array_data = self.classification.get_many_seconds()

        print '{}:'.format(self.saveFolder.rpartition('/')
                           [0].rpartition('/')[2])

        labels = self._get_labels(
            self.randomList, self.imageList, self.classification.seconds)

        with open(self.saveFolder+'dataset.csv', 'w') as dataset_file:
            for index, data in enumerate(tqdm(array_data)):
                if len(data) > 0:
                    data = map(list, zip(*data))
                    (delta, theta, alpha, beta) = get_frequency(data)
                    wave_data = get_feature(delta, theta, alpha, beta, False)
                    wr = csv.writer(dataset_file)
                    wave_data_with_label = np.insert(
                        wave_data, 0, labels[index])
                    wr.writerow(wave_data_with_label)

    def merge_files(self, save_folder, filenames):

        print "Create Full Dataset:"

        if not os.path.exists(save_folder):
            os.mkdir(save_folder)

        total = 0
        for sample in filenames:
            if sample.rpartition('/')[0].rpartition('/')[2] != 'full':
                total += sum(1 for row in open(sample+'dataset.csv'))

        pbar = tqdm(total=total)

        with open(save_folder+'dataset.csv', 'w') as file_out:
            for sample in filenames:
                if sample.rpartition('/')[0].rpartition('/')[2] != 'full':
                    wr = csv.writer(file_out)

                    file_csv = open(sample+'dataset.csv')
                    file_csv = csv.reader(file_csv)
                    file_csv = np.array([np.array(row) for row in file_csv])

                    for line in file_csv:
                        wr.writerow(line)
                        pbar.update(1)
        pbar.close()
