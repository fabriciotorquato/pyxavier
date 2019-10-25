#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import csv

import numpy as np


def get_time_classification(path):
    file_csv = open(path)
    data_csv = csv.reader(file_csv)
    data_csv = np.array([np.array(row) for row in data_csv])
    timestamps = []
    for row in data_csv:
        temp = row[0].split(" ")
        timestamps.append(temp[0]+" "+temp[3]+" "+temp[4])
    return timestamps


def get_data_classification(path, path_2):
    file_csv = open(path)
    data_csv = csv.reader(file_csv)
    data_csv = np.array([np.array(row) for row in data_csv])
    file_csv = open(path_2)
    data_csv_2 = csv.reader(file_csv)
    data_csv_2 = np.array([np.array(row) for row in data_csv_2])
    timestamps = []
    for idx, row in enumerate(data_csv):
        temp = row[0].split(" ")
        if temp[1] == "Negative":
            timestamps.append("0,"+data_csv_2[idx][0].split(" ", 1)[1])
        if temp[1] == "Neutral":
            timestamps.append("1,"+data_csv_2[idx][0].split(" ", 1)[1])
        if temp[1] == "Positive":
            timestamps.append("2,"+data_csv_2[idx][0].split(" ", 1)[1])

    return timestamps


def saveImageClassification(savePath, arrayFile):
    with open('{}classification.txt'.format(savePath), "w") as file:
        [file.write(value + "\n") for value in arrayFile]
    print("Image Classification Convert - Success")


def saveDataList(savePath, arrayFile):
    with open('{}dataList.csv'.format(savePath), "w") as file:
        [file.write(value + "\n") for value in arrayFile]
    print("Data List Convert - Success")
