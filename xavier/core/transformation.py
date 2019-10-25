#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from scipy.signal import butter, lfilter
from sklearn.preprocessing import StandardScaler


def fast_fourier_transform(all_channel_data):
    data_fft = map(lambda x: np.fft.fft(x), all_channel_data)
    return data_fft


def get_frequency(all_channel_data):

    # Length data channel
    L = len(all_channel_data[0])
    # Sampling frequency
    data_fft = fast_fourier_transform(all_channel_data)

    # Compute frequency
    frequency = map(lambda x: np.absolute(x / L), data_fft)
    frequency = map(lambda x: x[: L / 2 + 1] * 2, frequency)

    # List frequency
    delta = map(lambda x: x[0: 4], frequency)
    theta = map(lambda x: x[4: 8], frequency)
    alpha = map(lambda x: x[8: 12], frequency)
    beta = map(lambda x: x[12: 30], frequency)

    return delta, theta, alpha, beta


def get_feature(delta, theta, alpha, beta, isShowBandPower=True):

    # Compute feature std
    delta_std = np.std(delta, axis=1)
    theta_std = np.std(theta, axis=1)
    alpha_std = np.std(alpha, axis=1)
    beta_std = np.std(beta, axis=1)

    # Compute feature mean
    delta_m = np.mean(delta, axis=1)
    theta_m = np.mean(theta, axis=1)
    alpha_m = np.mean(alpha, axis=1)
    beta_m = np.mean(beta, axis=1)

    if isShowBandPower:
        print_wave(delta_std, theta_std, alpha_std, beta_std, "std")

    feature = np.array([delta_std, delta_m, theta_std,
                        theta_m, alpha_std, alpha_m, beta_std, beta_m])

    feature = feature.T
    feature = feature.ravel()

    return feature


def print_wave(delta, theta, alpha, beta, type, sensor_index=0):

    print str(type) + "-delta-" + str(sensor_index) + \
        ": " + str(delta[sensor_index])
    print str(type) + "-theta-" + str(sensor_index) + \
        ": " + str(theta[sensor_index])
    print str(type) + "-alpha-" + str(sensor_index) + \
        ": " + str(alpha[sensor_index])
    print str(type) + "-beta-" + str(sensor_index) + \
        ": " + str(beta[sensor_index])

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=3):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y


def get_filter(x):
    fs = 128.0

    # Alpha wave 8 hz ~ 12 hz
    lowcut = 8
    highcut = 12

    return butter_bandpass_filter(x, lowcut, highcut, fs, order=2)


def get_standard(data, standard):
    data = standard.transform(data)
    return data


def init_standard(data):
    standard = StandardScaler().fit(data)
    return get_standard(data, standard), standard
