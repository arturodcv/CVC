#!/usr/bin/env python3

import numpy as np
import math
import pandas as pd
import os
import time
from glob import glob
import shutil
#from tqdm import tqdm
import pickle

from nest_values import *
from funciones   import *


#import datatable as dt

############################################################ Move Files #######################################################################

create_folder(sd_path); #remove_contents(sd_path)
create_folder(df_folder); #remove_contents(df_folder)
create_folder(positions_path); #remove_contents(positions_path)

    
########################################################### Read files ###################################################################

positions = pd.read_csv('positions_df.txt', sep = ' ')
layers_to_record = load_dict('to_record_layer')
spike_detectors = load_dict('to_record_sd')
with open('seed.txt') as f:
    msd = int(f.readlines()[0])


######################################################### To dataframe ###################################################################

data_to_df(images_selected, positions, spike_detectors, layers_to_record, msd)

print('Tiempo tratamiento de datos: '+str(np.around(time.time() - t)) + ' s')


print("\nExc / Inh / Total number of spikes: ", sum(exc_activity), sum(inh_activity), sum(lengths)); print("\n")





