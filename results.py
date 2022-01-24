#!/usr/bin/env python3
import cv2
import numpy as np
import matplotlib.pyplot as plt
import math
import pandas as pd
import os
from PIL import Image
import time
from glob import glob
import shutil
from tqdm import tqdm
from collections import Counter
from collections import OrderedDict
from scipy.fft import rfft
import pickle
import scipy.signal

from nest_values import *
from funciones   import *


########################### results for exc/inh/total 

print("Results for total data: ")
path = results_path + '/data_total'; create_folder(path) ; remove_contents(path)   

data = read_and_fix_dataframe('','total')
times,complementary_time_list = get_times(data)
eeg = get_eeg(times, complementary_time_list, 'total', '_', path)
freqs, peaks, values, idx = get_frequencies(eeg,'total','_', path)
total_activity = np.sum(eeg)

print("\n\nResults for inhibitory data: ")
path = results_path + '/data_inh'; create_folder(path) ; remove_contents(path)

data = read_and_fix_dataframe('','inh')
times,complementary_time_list = get_times(data)
eeg = get_eeg(times, complementary_time_list, 'inh', '_', path)
freqs, peaks,values, idx = get_frequencies(eeg,'inh','_', path)
inh_activity = np.sum(eeg)
print('inhibitory spikes: ',np.sum(eeg[200:]))

print("\n\nResults for excitatory data: ")

path = results_path + '/data_exc'; create_folder(path) ; remove_contents(path)

data = read_and_fix_dataframe('','exc')
times,complementary_time_list = get_times(data)
eeg = get_eeg(times, complementary_time_list, 'exc', '_', path)
freqs, peaks, values, idx = get_frequencies(eeg,'exc','_', path)
exc_activity = np.sum(eeg)
print('excitatory spikes: ',np.sum(eeg[200:]))

collect_data(eeg, image_selected, exc_activity, inh_activity, peaks, values, idx)

#################### results for orientations

quit()
orientations = [i*180/num_orientations for i in range(0,num_orientations)]
neuron_types = ['l_exc', 'l_inh']

for orientation_to_read in orientations:
    for exc_or_inh in neuron_types:
        
        path = results_path + '/results_' + str(orientation_to_read) + '_' + str(exc_or_inh)
        create_folder(path); remove_contents(path)

        data = read_and_fix_dataframe(orientation_to_read,exc_or_inh)

        if len(data) < 2:
            continue
        times = generate_frames(data)
        frames, complementary_time_list = generate_empty_frames(times)
        img_array = read_frames(frames)
        create_video(img_array,orientation_to_read ,exc_or_inh, path)
        create_avg_img(img_array,orientation_to_read ,exc_or_inh , path)
        #eeg = get_eeg(times, complementary_time_list, orientation_to_read, exc_or_inh, path)
        #freqs = get_frequencies(eeg,orientation_to_read,exc_or_inh, path)
        

print("\n")




