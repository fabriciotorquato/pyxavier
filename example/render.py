#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import time
from argparse import ArgumentParser
try:
    from xavier.plot.render import Render
except:
    sys.path.insert(0, os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..')))
    from xavier.plot.render import Render


def startRender():
    render.start()


def stopRender():
    render.stop()


def get_args():
    parser = ArgumentParser(description='Xavier')
    parser.add_argument('--model', type=str, default='')
    parser.add_argument('--type_nn', type=str, default='')
    parser.add_argument('--path', type=str, default='')
    parser.add_argument('--username', type=str, default='')
    parser.add_argument('--train', type=bool, default=False)
    parser.add_argument('--ip', type=str, default='127.0.0.1:8080')
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = get_args()

    model = args.model
    type_nn = args.type_nn
    path = args.path
    username = args.username
    train = args.train
    ip = args.ip

    try:
      render = Render(model=model, type_nn=type_nn,
                    path=path, username=username, isTrain=train, ip=ip)
      startRender()
    except Exception as ex:
      print ex

