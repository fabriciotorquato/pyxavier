#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import csv
import numpy as np
import os
from glob import glob
from xavier.core.convert import saveImageClassification, saveDataList, get_time_classification, get_data_classification

if __name__ == "__main__":

    type = sys.argv[1]

    path_to_directory = 'dataset/'+type+'/'
    filenames = glob(os.path.join(path_to_directory, "*", ""))

    for idx, file in enumerate(filenames):
        
        classification = file+"image_classification.txt"
        data_random = file+"data_random.txt"

        saveImageClassification(file, get_time_classification(classification))
        saveDataList(file, get_data_classification(
            classification, data_random))
