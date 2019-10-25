#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import torch
from torch.utils.data.sampler import SubsetRandomSampler

torch.manual_seed(1234)


class DataLoader(object):
    def get_train(self, train_dataset,
                  batch_size,
                  valid_size=0.2,
                  shuffle=True,
                  num_workers=2,
                  pin_memory=False):

        num_train = len(train_dataset)
        indices = list(range(num_train))
        split = int(np.floor(valid_size * num_train))

        if shuffle:
            np.random.shuffle(indices)

        train_idx, valid_idx = indices[split:], indices[:split]
        train_sampler = SubsetRandomSampler(train_idx)
        valid_sampler = SubsetRandomSampler(valid_idx)

        train_loader = torch.utils.data.DataLoader(
            train_dataset, batch_size=batch_size, sampler=train_sampler, num_workers=num_workers, pin_memory=pin_memory)

        valid_loader = torch.utils.data.DataLoader(
            train_dataset, batch_size=batch_size, sampler=valid_sampler, num_workers=num_workers, pin_memory=pin_memory)

        return (train_loader, valid_loader, len(train_idx), len(valid_idx))

    def get_test(self, dataset,
                 batch_size,
                 shuffle=True,
                 num_workers=2,
                 pin_memory=False):

        data_loader = torch.utils.data.DataLoader(
            dataset, batch_size=batch_size, shuffle=shuffle,
            num_workers=num_workers, pin_memory=pin_memory,
        )

        return data_loader
