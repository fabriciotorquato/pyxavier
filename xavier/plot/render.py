#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

import xavier.constants.eeg as eeg
from xavier.constants.type import Type
from xavier.lib.emokit.emotiv import Emotiv
from xavier.lib.emokit.packet import EmotivExtraPacket
from xavier.plot.grapher import Grapher


class Render(object):
    def __init__(self, model, type_nn, path="", username="", isTrain=False, ip=""):
        self._stop_render = False
        self._model = model
        self._path = path
        self._username = username
        self._ip = ip
        self._isTrain = isTrain

        self._type_nn = None
        if type_nn == "mlp":
            self._type_nn = Type.mlp
        elif type_nn == "rnn":
            self._type_nn = Type.rnn
        elif type_nn == "cnn":
            self._type_nn = Type.cnn

    def start(self):
        self._stop_render = False
        counter = 0
        try:
            grapher = Grapher(self._model, self._type_nn,
                              self._isTrain, self._ip)

            with Emotiv(display_output=False, verbose=True, write=self._isTrain, output_path=self._path + "/" + self._username + "/") as emotiv:
                while emotiv.running:
                    if self._stop_render:
                        emotiv.stop()
                        return
                    packet = emotiv.dequeue()
                    if packet is not None and type(packet) != EmotivExtraPacket:
                        grapher.update(packet)
                        counter += 1
                        if counter == eeg.SAMPLING_RATE:
                            grapher.draw(eeg.WINDOW_SIZE)
                            counter = 0

                    time.sleep(0.001)
        except Exception as ex:
            print '{}'.format(ex)
            emotiv.stop()
            return
        finally:
            emotiv.stop()
            return

    def stop(self):
        self._stop_render = True
