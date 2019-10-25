#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import threading

import numpy as np

import xavier.constants.eeg as eeg
from xavier.core.training import Training as ModelTraining
from xavier.core.transformation import get_feature, get_filter, get_frequency


class Grapher(object):
    def __init__(self, path_model, type, isTrain=False, ip=""):
        self.path_model = path_model
        self.fullBuffer = []
        self.type = type
        self.isTrain = isTrain
        if ip:
            self.ip, self.port = ip.split(":")
            self.port = int(self.port)
        else:
            self.ip = None
        self.listResults = []
        self.sensors = eeg.SENSOR_NAME.split(' ')
        if not self.isTrain:
            self.init_model()

    def update(self, packet):
        values = []
        for name in self.sensors:
            values.append(packet.sensors[name]['value'])
        self.fullBuffer.append(values)

    def modification(self, buffer):
        data = np.array(buffer)
        data = data.T
        data = data.astype(np.float64)
        return data

    def draw(self, size, index_sensor=0):
        all_channel_data = self.modification(self.fullBuffer)
        self.fullBuffer = self.fullBuffer[-size:]

        (delta, theta, alpha, beta) = get_frequency(all_channel_data)

        threading.Thread(target=self.waveDraw, args=(
            self.sensors[index_sensor], all_channel_data[index_sensor], size)).start()

        threading.Thread(target=self.process_wave, args=(
            delta, theta, alpha, beta)).start()

    def waveDraw(self, sensor_name, waveValues, size):
        data_filter = get_filter(waveValues)[-size:]
        for data in data_filter:
            print '{}:{}'.format(sensor_name, data)

    def init_model(self):
        try:
            self.model_training = ModelTraining()
            self.model_training.load_model(self.type, self.path_model)
        except Exception as ex:
            print '{}'.format(ex)

    def process_wave(self, delta, theta, alpha, beta):
        feature = get_feature(delta, theta, alpha, beta)

        if not self.isTrain:
            result = self.model_training.predict(feature)

            print 'value: {}'.format(result)

            if self.ip:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((self.ip, self.port))
                    s.send(result)
                    s.close()
                except Exception as ex:
                    print '{}'.format(ex)
